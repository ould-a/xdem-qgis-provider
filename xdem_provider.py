from qgis.core import QgsProcessingProvider
from .algorithms.xdem_coregistration import *
from .algorithms.xdem_terrain_attributes import *


class XDemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # Terrain Attributes
        self.addAlgorithm(Slope())
        self.addAlgorithm(Aspect())
        self.addAlgorithm(Hillshade())
        
        # Coregistration
        self.addAlgorithm(Icp())
        self.addAlgorithm(Lzd())
        self.addAlgorithm(NuthKaab())

        # Tests
        self.addAlgorithm(BlockwiseNk())

    def id(self):
        return 'XDEM'

    def name(self):
        return self.tr('xDEM')

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
