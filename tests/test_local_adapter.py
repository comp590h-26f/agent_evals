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

from eval_adapters.local import LocalCliAgent, stage_package


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
            "AGENTS590_TRAJECTORY_PATH": "/logs/agent/trajectory.json",
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


def test_run_forwards_the_task_skills_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent = LocalCliAgent(logs_dir=tmp_path, agent="another-agent", skills_dir="/skills")
    assert agent.capabilities.skills
    seen: list[dict[str, str]] = []

    async def execute(
        environment: BaseEnvironment, command: str, env: dict[str, str], cwd: str | None = None
    ) -> ExecResult:
        seen.append(env)
        return ExecResult(return_code=0, stdout="", stderr="")

    monkeypatch.setattr(agent, "exec_as_agent", execute)
    environment = cast(BaseEnvironment, RecordingEnvironment())
    asyncio.run(agent.run("go", environment, AgentContext()))
    assert seen[0]["AGENTS590_SKILLS_DIR"] == "/skills"


def _trajectory(*usages: tuple[int, int]) -> str:
    steps: list[dict[str, object]] = [{"step_id": 1, "source": "user", "message": "go"}]
    steps += [
        {
            "step_id": index,
            "source": "agent",
            "message": "",
            "metrics": {"prompt_tokens": prompt, "completion_tokens": completion},
        }
        for index, (prompt, completion) in enumerate(usages, start=2)
    ]
    agent = {"name": "morty", "version": "0.1.0", "model_name": "deployment"}
    return json.dumps({"schema_version": "ATIF-v1.8", "agent": agent, "steps": steps})


def test_post_run_reports_tokens_from_the_trajectory(tmp_path: Path) -> None:
    (tmp_path / "trajectory.json").write_text(_trajectory((30, 7), (10, 2)))
    context = AgentContext()
    LocalCliAgent(logs_dir=tmp_path, agent="morty").populate_context_post_run(context)
    assert (context.n_input_tokens, context.n_output_tokens) == (40, 9)
    assert context.metadata == {"agent": "morty"}


def test_post_run_without_a_trajectory_reports_no_tokens(tmp_path: Path) -> None:
    context = AgentContext()
    LocalCliAgent(logs_dir=tmp_path, agent="krisj_echo").populate_context_post_run(context)
    assert (context.n_input_tokens, context.n_output_tokens) == (None, None)
    assert context.metadata == {"agent": "krisj_echo"}


def test_missing_package_fails_before_environment_setup(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="package_path"):
        stage_package(tmp_path / "missing", tmp_path)
