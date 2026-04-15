import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination)


METHODS = {'Deramping': xdem.coreg.Deramp(),
           'Directional biases' : xdem.coreg.DirectionalBias(),
           'Terrain biases': xdem.coreg.TerrainBias()}


class BiasCorrection(XdemProcessingAlgorithm):

    def tags(self):
        return METHODS

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_1',
            description='DEM to be aligned'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM_2',
            description='Reference DEM'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='INLIER_MASK',
            description='Inlier mask',
            defaultValue=None,
            optional=True))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='METHOD',
            description='Method',
            options=METHODS,
            defaultValue='Deramping',
            usesStaticStrings=True))

        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_path = (self.parameterAsLayer(parameters, 'DEM_1', context)).source()
        ref_dem_path = (self.parameterAsLayer(parameters, 'DEM_2', context)).source()
        method = self.parameterAsString(parameters, 'METHOD', context)
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = None

        try:
            inlier_mask_path = (self.parameterAsRasterLayer(parameters, 'INLIER_MASK', context)).source()
            inlier_mask = gu.Raster(inlier_mask_path, is_mask=True)
        except:
            feedback.pushWarning("Inlier Mask not provided")
            pass

        coreg = METHODS[method]

        coreg.fit(ref_dem, tba_dem, inlier_mask)
        aligned_dem = coreg.apply(tba_dem)
        coreg_info(coreg, feedback)

        aligned_dem.to_file(output_path)

        return {}
    
    def name(self):
        return 'Bias correction'
    
    def shortHelpString(self):
        return "This algorithm aim at correcting both systematic elevation errors and spatially-structured random errors."

    def createInstance(self):
        return BiasCorrection()
