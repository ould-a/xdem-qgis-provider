import xdem

from .xdem_tools import XdemProcessingAlgorithm, dem_info

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


class GapFilling(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='TBF_DEM',
            description='DEM to be filled'))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Filled DEM'))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, 'TBF_DEM', context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        dem = xdem.DEM(dem_path)
        dem_info(dem, feedback)

        ddem = xdem.dDEM(raster=dem, start_time=None, end_time=None)

        filled_array = ddem.interpolate(method="idw")

        filled_dem = xdem.DEM.from_array(filled_array, transform=dem.transform, crs=dem.crs)

        filled_dem.to_file(output_path)

        return {'OUTPUT': output_path}
    
    def name(self):
        return 'Gap filling'

    def shortHelpString(self):
        return "This algorithm uses the IDW (Inverse-distance weighting) method.\n" \
        "Empty areas are filled with a weighted average of the surrounding pixel values, with the weight being inversely proportional to their distance from the empty pixel."

    def createInstance(self):
        return GapFilling()
