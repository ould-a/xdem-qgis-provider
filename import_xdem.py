import os
import sys
import numpy
import pyproj

# Path Configuration
PLUGIN_DIR = os.path.dirname(__file__)
LIBS_FILE_NAME = "xdem_libs"
LIBS_DIR = os.path.join(PLUGIN_DIR, LIBS_FILE_NAME)

# Dependencies to install, xdem refers with the versions of dependencies shared with QGIS
REQUIRED_PACKAGES = [
    f"numpy=={numpy.__version__}",
    f"pyproj=={pyproj.__version__}",
    "xdem",
    "scikit-learn",
]

def _install_packages():
    """
    Function to install xdem package and shared dependencies.
    """

    for package in REQUIRED_PACKAGES:
        from pip._internal.cli.main import main as pip_main
        pip_main(["install", "--target", LIBS_DIR, package])

def check_xdem():
    """
    Function to check if xdem is already installed, if not, proceed with the installation and add it in QGIS.
    """
    
    if "xdem" in sys.modules:
        return sys.modules["xdem"]

    if not os.path.exists(LIBS_DIR):
        os.makedirs(LIBS_DIR, exist_ok=True)
        _install_packages()

    if LIBS_DIR not in sys.path:
        sys.path.insert(0, LIBS_DIR)

    try:
        import xdem
        return xdem
    except ImportError:
        raise

# xDEM import variable
xdem_package = check_xdem()
