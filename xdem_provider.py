from qgis.core import QgsProcessingProvider

from .algorithms.xdem_coreg import *
from .algorithms.xdem_terrain_attributes import *
from .algorithms.xdem_tools import *


class XDemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(BiasCorrection())
        self.addAlgorithm(Coregistration())
        self.addAlgorithm(TerrainAttributes())
        
    def id(self):
        return 'XDEM'

    def name(self):
        return self.tr('xDEM')

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
