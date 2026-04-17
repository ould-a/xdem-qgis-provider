from qgis.core import QgsProcessingProvider

from .algorithms.xdem_corrections import BiasCorrection, Coregistration, GapFilling
from .algorithms.xdem_terrain_attributes import Slope
from .algorithms.xdem_workflows import TopoWorkflow

class XdemProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        # DEM Analysis 
        self.addAlgorithm(Slope())

        # DEM Corections
        self.addAlgorithm(BiasCorrection())
        self.addAlgorithm(Coregistration())
        self.addAlgorithm(GapFilling())
        
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
