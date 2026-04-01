from qgis.core import QgsProcessingProvider
from .algorithms.xdem_coregistration import *
from .algorithms.xdem_terrain_attributes import *
from .algorithms.xdem_tools import *


class XDemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # Terrain Attributes
        self.addAlgorithm(TerrainAttributes())

        # Coregistration
        self.addAlgorithm(Coregistration())

        # Old versions
        self.addAlgorithm(Icp())
        self.addAlgorithm(Lzd())
        self.addAlgorithm(NuthKaab())

        self.addAlgorithm(Slope())
        self.addAlgorithm(Aspect())
        self.addAlgorithm(Hillshade())
        
    def id(self):
        return 'XDEM'

    def name(self):
        return self.tr('xDEM')

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
