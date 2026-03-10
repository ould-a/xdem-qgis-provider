from qgis.core import QgsProcessingProvider

from .xdem_algorithms import *

class XDemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # Terrain attributes
        self.addAlgorithm(Aspect())
        self.addAlgorithm(Hillshade())
        self.addAlgorithm(Slope())

        # Coregistration
        self.addAlgorithm(Icp())
        self.addAlgorithm(Lzd())
        self.addAlgorithm(NuthKaab())

    def id(self):
        return 'XDEM'

    def name(self):
        return self.tr('xDEM')

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
