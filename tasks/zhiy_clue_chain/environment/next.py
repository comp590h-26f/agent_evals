"""Show the current clue, or submit an answer to it."""

import hashlib
import json
import sys
from pathlib import Path

CHAIN_PATH = Path("/app/chain.dat")
STATE_PATH = Path("/app/.chain_state.json")
INITIAL_KEY = "start"


def derive_key(key: str, answer: str) -> str:
    return hashlib.sha256(f"{key}:{answer}".encode()).hexdigest()


def check_value(key: str) -> str:
    return hashlib.sha256(f"check:{key}".encode()).hexdigest()


def xor_with_key(data: bytes, key: str) -> bytes:
    stream = b""
    counter = 0
    while len(stream) < len(data):
        stream += hashlib.sha256(f"{key}:{counter}".encode()).digest()
        counter += 1
    return bytes(a ^ b for a, b in zip(data, stream, strict=False))


def main() -> int:
    chain = json.loads(CHAIN_PATH.read_text())
    if STATE_PATH.exists():
        state = json.loads(STATE_PATH.read_text())
    else:
        state = {"step": 0, "key": INITIAL_KEY, "text": chain["first_clue"]}

    total = len(chain["records"])
    if state["step"] >= total:
        print(f"Chain complete. Final token: {state['text']}")
        return 0

    if len(sys.argv) == 1:
        print(f"Clue {state['step'] + 1}/{total}: {state['text']}")
        return 0

    answer = " ".join(sys.argv[1:]).strip().lower()
    key = derive_key(state["key"], answer)
    record = chain["records"][state["step"]]
    if check_value(key) != record["check"]:
        print(f"Incorrect. Clue {state['step'] + 1}/{total}: {state['text']}")
        return 1

    text = xor_with_key(bytes.fromhex(record["payload"]), key).decode()
    state = {"step": state["step"] + 1, "key": key, "text": text}
    STATE_PATH.write_text(json.dumps(state))
    if state["step"] >= total:
        print(f"Chain complete. Final token: {text}")
    else:
        print(f"Correct. Clue {state['step'] + 1}/{total}: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
