from qgis.core import QgsProcessingProvider
from .algorithms.xdem_corrections import *
from .algorithms.xdem_terrain_attributes import *
from .algorithms.xdem_uncertainty import *
from .algorithms.xdem_workflows import *

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
        self.addAlgorithm(Aspect())
        self.addAlgorithm(FlowlineCurvature())
        self.addAlgorithm(FractalRoughness())
        self.addAlgorithm(GetTerrainAttributes())
        self.addAlgorithm(Hillshade())
        self.addAlgorithm(MaxCurvature())
        self.addAlgorithm(MinCurvature())
        self.addAlgorithm(PlanformCurvature())
        self.addAlgorithm(ProfileCurvature())
        self.addAlgorithm(Roughness())
        self.addAlgorithm(Rugosity())
        self.addAlgorithm(Slope())
        self.addAlgorithm(TangentialCurvature())
        self.addAlgorithm(TerrainRuggednessIndex())
        self.addAlgorithm(TextureShading())
        self.addAlgorithm(TopographicPositionIndex())

        # Uncertainty
        self.addAlgorithm(Heteroscedasticity())

        # Workflows
        self.addAlgorithm(AccuracyWorkflow())
        self.addAlgorithm(TopoWorkflow())

    def id(self):
        return "XDEM"

    def name(self):
        return self.tr("xDEM")

    def icon(self):
        return QgsProcessingProvider.icon(self)

    def longName(self):
        return self.name()
