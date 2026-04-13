import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, dem_info

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination)


METHODS = ['idw',
           'local_hypsometric',
           'regional_hypsometric']


class GapFilling(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_1',
            description='DEM to be filled'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_2',
            description='Reference DEM'))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='METHOD',
            description='Method',
            options=METHODS,
            defaultValue=METHODS[0],
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Filled DEM'))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_path = (self.parameterAsRasterLayer(parameters, 'DEM_1', context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'DEM_2', context)).source()
        method = self.parameterAsString(parameters, 'METHOD', context)

        self.output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        dem = xdem.dDEM(dem_path)
        ref_dem = xdem.dDEM(ref_dem_path)

        filled_dem = dem.interpolate(method=method)

        filled_dem.to_file(self.output_path)

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        iface.addRasterLayer(self.output_path)
        return {}
    
    def name(self):
        return 'Gap Filling'

    def shortHelpString(self):
        return "/"

    def createInstance(self):
        return GapFilling()