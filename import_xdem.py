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

REQUIRED_PACKAGES = [
    "xdem",
    "scikit-learn",
    "scikit-gstat",
]

# Packages QGIS provided by default
SHARED_PACKAGES = [
    "numpy",
    "pyproj",
    "rasterio",
    "pandas",
    "geopandas",
    "shapely"]


def _exist_in_qgis(package):
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False


def _clean_conflict_packages():
    removed_packages = []

    for xdem_package in os.listdir(LIBS_DIR):

        for shared_package in SHARED_PACKAGES:
            
            if _exist_in_qgis(shared_package):
                if xdem_package == shared_package or xdem_package.startswith(shared_package):
                    removed_packages.append(shared_package)
                    target_package = os.path.join(LIBS_DIR, xdem_package)
                    shutil.rmtree(target_package)

    return removed_packages


def _install_package():
    for package in REQUIRED_PACKAGES:
        pip_main(["install", "--target", LIBS_DIR, package])
    removed = _clean_conflict_packages()
    iface.messageBar().pushMessage(f"Conflicting dependencies:{removed}", level=Qgis.Info)


def check_xdem():
    if "xdem" in sys.modules:
        return sys.modules["xdem"]

    if not os.path.isdir(LIBS_DIR):
        os.makedirs(LIBS_DIR, exist_ok=True)
        try:
            _install_package()
        except:
            shutil.rmtree(LIBS_DIR, ignore_errors=True)

    if LIBS_DIR not in sys.path:
        sys.path.insert(0, LIBS_DIR)

    try:
        import xdem
        return xdem
    except ImportError:
        raise


# xDEM import variable
xdem_package = check_xdem()
