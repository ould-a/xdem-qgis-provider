import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, dem_info

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


class UncertaintyAnalysis(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_1',
            description='Aligned DEM'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_2',
            description='Reference DEM'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='STABLE_TERRAIN',
            description='Stable terrain'))

        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Error map variability'))

    def processAlgorithm(self, parameters, context, feedback):
        aligned_dem_path = (self.parameterAsLayer(parameters, 'DEM_1', context)).source()
        ref_dem_path = (self.parameterAsLayer(parameters, 'DEM_2', context)).source()
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        aligned_dem = xdem.DEM(aligned_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)
        dem_info(aligned_dem, feedback)

        try:
            stable_terrain_path = (self.parameterAsLayer(parameters, 'STABLE_TERRAIN', context)).source()
            stable_terrain = gu.Raster(stable_terrain_path, is_mask=True)
        except:
            pass

        sig_dem, rho_sig = aligned_dem.estimate_uncertainty(ref_dem, stable_terrain=stable_terrain, precision_of_other='same')

        feedback.pushInfo("Random elevation errors at a distance of 1 km are correlated at {:.2f} %.".format(rho_sig(1000) * 100))

        sig_dem.to_file(output_path)
        
        return {}
    
    def name(self):
        return 'Uncertainty analysis'

    def shortHelpString(self):
        return "This algorithm estimates, models and returns a map of variable error matching the DEM.\n" \
        "It is based on the method: Hugonnet et al. (2022)"

    def createInstance(self):
        return UncertaintyAnalysis()
