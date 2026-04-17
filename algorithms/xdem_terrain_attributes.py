import xdem

from .xdem_tools import XdemProcessingAlgorithm

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


class Slope(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="DEM",
            description="DEM"))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name="OUTPUT",
            description="Slope"))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, "DEM", context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        output_path = self.parameterAsOutputLayer(parameters, "OUTPUT", context)

        dem = xdem.DEM(dem_path)

        slope = dem.slope()
        slope.to_file(output_path)

        return {"OUTPUT": output_path}
    
    def name(self):
        return "Slope"
    
    def groupId(self):
        return "Terrain attributes"

    def createInstance(self):
        return Slope()