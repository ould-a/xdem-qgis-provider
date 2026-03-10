import subprocess
import os
import sys

from .xdem_config import (PLUGINDIR,
                          VENVNAME,
                          VENVDIR,
                          PY_XDEM)

def classFactory(iface):
    from .xdem_plugin import XDemPlugin
    return XDemPlugin()

# Virtual environment configuation
def setupxdemvenv():
    if VENVNAME not in os.listdir(PLUGINDIR):
        subprocess.run([sys.executable, "-m", "venv", VENVDIR])
        subprocess.Popen([PY_XDEM, "pip", "install", "--upgrade", "pip"])
        subprocess.Popen([PY_XDEM, "-m", "pip", "install", "xdem"])

setupxdemvenv()