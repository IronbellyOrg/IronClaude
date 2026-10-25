import tempfile
from pathlib import Path
from superclaude import ReflexionPattern

with tempfile.TemporaryDirectory() as tmp:
    # Nest the memory dir so the sibling "mistakes" folder also stays inside tmp.
    reflexion = ReflexionPattern(memory_dir=Path(tmp) / "docs" / "memory")

    error_info = {
        "error_type": "ValueError",
        "error_message": "invalid port value 9090 in config file",
        "test_name": "test_load_config",
    }

    known = reflexion.get_solution(error_info)   # None: the temporary store is empty
    if known is None:
        error_info["solution"] = "Validate the port before binding"
        error_info["root_cause"] = "Config loader accepted any string"
        reflexion.record_error(error_info)       # appends a row, adds "timestamp"

print("snippet-ok known=", known)
