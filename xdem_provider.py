from qgis.core import QgsProcessingProvider

from .algorithms.xdem_corrections import BiasCorrection, Coregistration, GapFilling
from .algorithms.xdem_terrain_attributes import GetTerrainAttributes, Aspect, Hillshade, Slope
from .algorithms.xdem_uncertainty import Heteroscedasticity, UncertaintyAnalysis
from .algorithms.xdem_workflows import TopoWorkflow

class XdemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # Corections
        self.addAlgorithm(BiasCorrection())
        self.addAlgorithm(Coregistration())
        self.addAlgorithm(GapFilling())

        # Terrain attributes
        #self.addAlgorithm(GetTerrainAttributes())
        self.addAlgorithm(Aspect())
        self.addAlgorithm(Hillshade())
        self.addAlgorithm(Slope())

        # Uncertainty
        self.addAlgorithm(Heteroscedasticity())
        self.addAlgorithm(UncertaintyAnalysis())
        
        # Workflows
        self.addAlgorithm(TopoWorkflow())
        
    def id(self):
        return "XDEM"

    def name(self):
        return self.tr("xDEM")

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
