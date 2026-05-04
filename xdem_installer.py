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
REQUIRED_PACKAGES = ["cerberus", "matplotlib", "pytest", "scikit-learn", "weasyprint", "xdem"]
SHARED_PACKAGES = ["numpy", "pyproj", "rasterio", "pandas", "geopandas", "shapely"]


def _exist_in_qgis(package):
    """
    Fnction that checks whether a package is present in QGIS by attempting to import it.
    """

    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False


def _clean_conflict_packages():
    """
    Function that removes shared packages if they exist in QGIS.
    """

    for xdem_package in os.listdir(LIBS_DIR):
        for shared_package in SHARED_PACKAGES:
            if _exist_in_qgis(shared_package):
                if xdem_package == shared_package or xdem_package.startswith(shared_package):
                    target_package = os.path.join(LIBS_DIR, xdem_package)
                    shutil.rmtree(target_package)


def _install_package():
    """
    Function that installs a package in the plugin directory.
    """

    for package in REQUIRED_PACKAGES:
        pip_main(["install", "--target", LIBS_DIR, package])
    iface.messageBar().pushMessage("xDEM dependencies successfully installed", level=Qgis.Info)


def check_xdem():
    """
    Function that checks if xdem is present, if not, it proceeds with the installation.
    """

    if "xdem" in sys.modules:
        return sys.modules["xdem"]
    if not os.path.isdir(LIBS_DIR):
        os.makedirs(LIBS_DIR, exist_ok=True)
        try:
            _install_package()
            _clean_conflict_packages()
        except:
            shutil.rmtree(LIBS_DIR, ignore_errors=True)
            iface.messageBar().pushMessage("xDEM dependencies could not be installed", level=Qgis.Critical)
    if LIBS_DIR not in sys.path:
        sys.path.insert(0, LIBS_DIR)
    try:
        import xdem
        return xdem
    except ImportWarning:
        iface.messageBar().pushMessage("xDEM dependencies could not be imported", level=Qgis.Critical)
        shutil.rmtree(LIBS_DIR, ignore_errors=True)
        return None


# xDEM install variable
xdem_package = check_xdem()
