"""Check local packaging, CLI forwarding, and credential handling without Docker."""

import asyncio
import json
import shlex
from pathlib import Path
from typing import cast

import pytest
from harbor.environments.base import BaseEnvironment, ExecResult
from harbor.models.agent.context import AgentContext
from harbor.models.task.config import EnvironmentConfig
from harbor.models.trajectories import Trajectory

from eval_adapters.local import LocalCliAgent, build_trajectory, stage_package


@pytest.fixture(params=["package", "package with spaces"])
def package_root(tmp_path: Path, request: pytest.FixtureRequest) -> Path:
    root = tmp_path / request.param
    for name in (
        "pyproject.toml",
        "README.md",
        "uv.lock",
        "src/agents590/__init__.py",
        "src/agents590/__pycache__/module.pyc",
        ".env",
        ".venv/secret",
        ".git/config",
        "jobs/result.json",
        "tests/test_agent.py",
    ):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(name)
    return root


class RecordingEnvironment:
    default_user: str | None = None
    task_env_config = EnvironmentConfig(workdir="/app")

    def __init__(self) -> None:
        self.files: set[str] = set()
        self.upload_target = ""

    async def upload_dir(self, source_dir: Path, target_dir: str) -> None:
        self.upload_target = target_dir
        self.files = {path.relative_to(source_dir).as_posix() for path in source_dir.rglob("*")}


def test_stage_contains_only_package_source(package_root: Path, tmp_path: Path) -> None:
    destination = tmp_path / "staged"
    destination.mkdir()
    stage_package(package_root, destination)
    files = {path.relative_to(destination).as_posix() for path in destination.rglob("*")}
    assert files == {
        "pyproject.toml",
        "README.md",
        "uv.lock",
        "src",
        "src/agents590",
        "src/agents590/__init__.py",
    }


def test_install_uses_a_local_snapshot(
    package_root: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent = LocalCliAgent(logs_dir=tmp_path, agent="krisj_echo", package_path=package_root)
    environment = RecordingEnvironment()
    commands: list[str] = []

    async def dependencies(environment: BaseEnvironment, names: tuple[str, ...]) -> None:
        assert names == ("curl",)

    async def execute(
        environment: BaseEnvironment, command: str, timeout_sec: int | None = None
    ) -> ExecResult:
        commands.append(command)
        return ExecResult(return_code=0, stdout="", stderr="")

    monkeypatch.setattr(agent, "ensure_system_dependencies", dependencies)
    monkeypatch.setattr(agent, "exec_as_root", execute)
    monkeypatch.setattr(agent, "exec_as_agent", execute)
    asyncio.run(agent.install(cast(BaseEnvironment, environment)))
    assert environment.upload_target == "/installed-agent/agents590/source"
    assert "src/agents590/__init__.py" in environment.files
    assert ".env" not in environment.files
    assert "uv sync --locked --no-dev" in commands[-1]
    assert "/installed-agent/agents590/source" in commands[-1]
    assert str(package_root) not in commands[-1]


def test_run_quotes_instruction_and_forwards_model_and_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("EXAMPLE_API_KEY=from-file\nOTHER_SETTING=preserved\n")
    agent = LocalCliAgent(
        logs_dir=tmp_path / "logs",
        agent="another-agent",
        model_name="openai/run-deployment",
        env_file=env_file,
        extra_env={"EXAMPLE_API_KEY": "explicit-override"},
    )
    environment = RecordingEnvironment()
    instruction = "Quotes ' and spaces; $(touch /app/unexpected)\nA second line"
    seen: list[list[str]] = []

    async def execute(
        environment: BaseEnvironment, command: str, env: dict[str, str], cwd: str | None = None
    ) -> ExecResult:
        seen.append(shlex.split(command))
        assert "explicit-override" not in command
        assert env == {
            "EXAMPLE_API_KEY": "explicit-override",
            "OTHER_SETTING": "preserved",
            "AGENTS590_LOG_DIR": "/logs/agent",
            "AGENTS590_ATIF_PATH": "/logs/agent/trajectory.json",
        }
        assert cwd == "/app"
        return ExecResult(return_code=0, stdout="agent result\n", stderr="")

    monkeypatch.setattr(agent, "exec_as_agent", execute)
    context = AgentContext()
    asyncio.run(agent.run(instruction, cast(BaseEnvironment, environment), context))
    assert seen == [
        [
            "/installed-agent/agents590/venv/bin/python",
            "-m",
            "agents590",
            "another-agent",
            "-i",
            instruction,
            "--model",
            "openai/run-deployment",
        ]
    ]
    assert (agent.logs_dir / "stdout.txt").read_text() == "agent result\n"
    assert context.is_empty()
    agent.populate_context_post_run(context)
    assert context.metadata == {"agent": "another-agent"}


def test_missing_package_fails_before_environment_setup(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="package_path"):
        stage_package(tmp_path / "missing", tmp_path)


def test_trace_lines_become_a_valid_atif_trajectory() -> None:
    from harbor.models.trajectories.trajectory import Trajectory

    from eval_adapters.local import build_trajectory

    turns = [
        {"tokens": [10, 4, 3], "text": "", "commands": [["ls", "a.py\n(exit code 0)"]]},
        {"tokens": [20, 0, 5], "text": "Done.", "commands": []},
    ]
    trajectory = Trajectory.model_validate(build_trajectory("Fix it", turns, "gpt"))

    assert [step.source for step in trajectory.steps] == ["user", "agent", "agent"]
    assert trajectory.steps[1].tool_calls[0].arguments == {"command": "ls"}  # type: ignore[index]
    assert trajectory.final_metrics is not None
    assert trajectory.final_metrics.total_prompt_tokens == 30
    assert trajectory.final_metrics.total_completion_tokens == 8


TRACE_TURN = {"tokens": [3, 1, 2], "text": "done", "commands": [["ls", "ok"]]}


def run_with_output(
    agent: LocalCliAgent, stdout: str, stderr: str, monkeypatch: pytest.MonkeyPatch
) -> AgentContext:
    async def execute(
        environment: BaseEnvironment, command: str, env: dict[str, str], cwd: str | None = None
    ) -> ExecResult:
        return ExecResult(return_code=0, stdout=stdout, stderr=stderr)

    monkeypatch.setattr(agent, "exec_as_agent", execute)
    context = AgentContext()
    environment = cast(BaseEnvironment, RecordingEnvironment())
    asyncio.run(agent.run("Do it", environment, context))
    agent.populate_context_post_run(context)
    return context


def test_malformed_trace_records_do_not_fail_the_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent = LocalCliAgent(logs_dir=tmp_path, agent="some-agent")
    stdout = f"TRACE {{malformed}}\nTRACE 1\nTRACE {json.dumps(TRACE_TURN)}\n"

    context = run_with_output(agent, stdout, 'TRACE {"tokens": [1]}\n', monkeypatch)

    assert (context.n_input_tokens, context.n_cache_tokens, context.n_output_tokens) == (3, 1, 2)
    assert len(json.loads((tmp_path / "trajectory.json").read_text())["steps"]) == 2


def test_only_malformed_trace_records_leave_no_trajectory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent = LocalCliAgent(logs_dir=tmp_path, agent="some-agent")

    context = run_with_output(agent, "TRACE {malformed}\n", "", monkeypatch)

    assert context.n_input_tokens is None
    assert not (tmp_path / "trajectory.json").exists()


def test_native_trajectory_and_cost_outrank_trace_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    native = build_trajectory("Do it", [{**TRACE_TURN, "tokens": [9, 0, 9]}], None)
    native["final_metrics"]["total_cost_usd"] = 0.25
    (tmp_path / "trajectory.json").write_text(json.dumps(native))
    agent = LocalCliAgent(logs_dir=tmp_path, agent="some-agent")

    context = run_with_output(agent, f"TRACE {json.dumps(TRACE_TURN)}\n", "", monkeypatch)

    assert (context.n_input_tokens, context.cost_usd) == (9, 0.25)


def test_event_journal_outranks_trace_records(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    journal = build_trajectory("Do it", [{**TRACE_TURN, "tokens": [7, 0, 7]}], None)
    agent = LocalCliAgent(logs_dir=tmp_path, agent="some-agent")
    monkeypatch.setattr(agent, "convert_trajectory", lambda _: Trajectory.model_validate(journal))

    context = run_with_output(agent, f"TRACE {json.dumps(TRACE_TURN)}\n", "", monkeypatch)

    assert context.n_input_tokens == 7
