import os
import sys
import shutil
import importlib

from pip._internal.cli.main import main as pip_main
from qgis.core import Qgis
from qgis.utils import iface


# Path Configuration
PLUGIN_DIR = os.path.dirname(__file__)
LIBS_FILE_NAME = "xdem_libs"
LIBS_DIR = os.path.join(PLUGIN_DIR, LIBS_FILE_NAME)

# Packages Configuration
REQUIRED_PACKAGES = ["xdem[opt]"]
REMOVABLE_PACKAGES = ["tqdm"]
SHARED_PACKAGES = ["numpy", "pyproj", "rasterio", "pandas", "geopandas", "shapely"]


def _exist_in_qgis(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False


def _clean_conflict_packages():
    for xdem_package in os.listdir(LIBS_DIR):
        for shared_package in SHARED_PACKAGES:
            if _exist_in_qgis(shared_package):
                if xdem_package == shared_package or xdem_package.startswith(shared_package):
                    target_package = os.path.join(LIBS_DIR, xdem_package)
                    shutil.rmtree(target_package)

def _clean_removable_packages():
    for xdem_package in os.listdir(LIBS_DIR):
        for removable_package in REMOVABLE_PACKAGES:
            if xdem_package == removable_package or xdem_package.startswith(removable_package):
                target_package = os.path.join(LIBS_DIR, xdem_package)
                shutil.rmtree(target_package)

def _install_package():
    for package in REQUIRED_PACKAGES:
        pip_main(["install", "--target", LIBS_DIR, package])
    iface.messageBar().pushMessage("xDEM dependencies successfully installed", level=Qgis.Info)


def check_xdem():
    if "xdem" in sys.modules:
        return sys.modules["xdem"]
    if not os.path.isdir(LIBS_DIR):
        os.makedirs(LIBS_DIR, exist_ok=True)
        try:
            _install_package()
            _clean_conflict_packages()
            _clean_removable_packages()
        except:
            shutil.rmtree(LIBS_DIR, ignore_errors=True)
    if LIBS_DIR not in sys.path:
        sys.path.insert(0, LIBS_DIR)
    try:
        import xdem
        return xdem
    except:
        iface.messageBar().pushMessage("xDEM dependencies could not be installed ", level=Qgis.Critical)
        shutil.rmtree(LIBS_DIR, ignore_errors=True)


# xDEM install variable
xdem_package = check_xdem()
