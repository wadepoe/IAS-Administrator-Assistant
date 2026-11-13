"""Test conftest — ensures app/ is on sys.path at collection time."""
import sys
from pathlib import Path

# Add app/ to sys.path at import/collection time so test modules can
# import from tools, agent, etc. as peer-level modules.
_app_path = str(Path(__file__).parent.parent / "app")
if _app_path not in sys.path:
    sys.path.insert(0, _app_path)
