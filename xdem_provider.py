from qgis.core import QgsProcessingProvider

from .algorithms.xdem_biascorr import BiasCorrection
from .algorithms.xdem_coregistration import Coregistration
from .algorithms.xdem_terrain_attributes import TerrainAttributes
from .algorithms.xdem_uncertainty import UncertaintyAnalysis
from .algorithms.xdem_gap_filling import GapFilling


class XDemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(BiasCorrection())
        self.addAlgorithm(GapFilling())
        self.addAlgorithm(Coregistration())
        self.addAlgorithm(TerrainAttributes())
        self.addAlgorithm(UncertaintyAnalysis())
        
    def id(self):
        return 'XDEM'

    def name(self):
        return self.tr('xDEM')

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
