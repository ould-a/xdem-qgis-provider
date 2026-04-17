# Initialization script

def classFactory(iface):
    from .import_xdem import xdem_package
    from .xdem_plugin import XdemPlugin
    return XdemPlugin()