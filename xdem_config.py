import os
import sys

PLUGINDIR = os.path.dirname(__file__)
VENVNAME = "venvxdem"
VENVDIR = os.path.join(PLUGINDIR, VENVNAME)
PY_SYS = sys.executable
PY_XDEM = os.path.join(VENVDIR, "bin", "python")
SUBPROCESS_SCRIPT = os.path.join(PLUGINDIR, "subprocess_script.py")