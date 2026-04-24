from qgis.core import QgsProcessingProvider

from .algorithms.xdem_corrections import BiasCorrection, Coregistration, GapFilling
from .algorithms.xdem_terrain_attributes import (Aspect, Hillshade, Slope, ProfileCurvature, TangentialCurvature, PlanformCurvature)
from .algorithms.xdem_uncertainty import Heteroscedasticity
from .algorithms.xdem_workflows import AccuracyWorkflow, TopoWorkflow

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
        self.addAlgorithm(Hillshade())
        self.addAlgorithm(Slope())
        self.addAlgorithm(ProfileCurvature())
        self.addAlgorithm(TangentialCurvature())
        self.addAlgorithm(PlanformCurvature())

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
