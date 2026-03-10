import subprocess
import os
import sys

from qgis.core import Qgis

from .xdem_config import (PLUGINDIR,
                          VENVNAME,
                          VENVDIR,
                          PY_XDEM)

def classFactory(iface):
    setupxdemvenv(iface)
    from .xdem_plugin import XDemPlugin
    return XDemPlugin()

# Virtual environment configuation
def setupxdemvenv(iface):
    if VENVNAME not in os.listdir(PLUGINDIR):
        subprocess.run([sys.executable, "-m", "venv", VENVDIR])
        subprocess.Popen([PY_XDEM, "-m", "ensurepip", "--upgrade"])
        subprocess.Popen([PY_XDEM, "-m", "pip", "install", "xdem"])
        iface.messageBar().pushMessage("Installing xdem dependencies, please wait a few seconds before using it.", level=Qgis.Info, duration=30)