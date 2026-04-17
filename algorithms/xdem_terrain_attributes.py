import xdem

from .xdem_tools import XdemProcessingAlgorithm

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)

attribute_param = {}

attributes = {
            "Slope": lambda x: x.dem.slope(**attribute_param),
            "Aspect": lambda x: x.dem.aspect(**attribute_param)}

class Slope(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="DEM",
            description="DEM"))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name="OUTPUT",
            description="Slope"))
        
    def processAlgorithm(self, parameters, context, feedback):
        return {}
    
    def name(self):
        return "Slope"
    
    def groupId(self):
        return "DEM Analysis"

    def shortHelpString(self):
        return "/"

    def createInstance(self):
        return Slope()