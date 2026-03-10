import os
import sys
import inspect

from qgis.core import QgsApplication
from .xdem_provider import XDemProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)


class XDemPlugin(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        self.provider = XDemProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
