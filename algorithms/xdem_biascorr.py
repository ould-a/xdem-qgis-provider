import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination)


BIAS_CORRECTION_METHODS = ['Deramping',
                           'Directional biases',
                           'Terrain biases']


class BiasCorrection(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='TBA_DEM',
            description='DEM to be aligned'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='REF_DEM',
            description='Reference DEM'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='INLIER_MASK',
            description='Inlier mask',
            defaultValue=None,
            optional=True))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='METHOD',
            description='Method',
            options=BIAS_CORRECTION_METHODS,
            defaultValue=BIAS_CORRECTION_METHODS[0],
            usesStaticStrings=True))

        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_path = (self.parameterAsRasterLayer(parameters, 'TBA_DEM', context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'REF_DEM', context)).source()
        method = self.parameterAsString(parameters, 'METHOD', context)

        self.output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = None

        try:
            inlier_mask_path = (self.parameterAsRasterLayer(parameters, 'INLIER_MASK', context)).source()
            inlier_mask = gu.Raster(inlier_mask_path, is_mask=True)
        except:
            feedback.pushWarning("Inlier Mask not provided")
            pass

        if method == 'Deramping':
            coreg = xdem.coreg.Deramp()

        elif method == 'Directional biases':
            coreg = xdem.coreg.DirectionalBias()

        elif method == 'Terrain biases':
            coreg = xdem.coreg.TerrainBias()

        coreg.fit(ref_dem, tba_dem, inlier_mask)
        aligned_dem = coreg.apply(tba_dem)
        coreg_info(coreg=coreg, feedback=feedback)
        aligned_dem.to_file(self.output_path)
        
        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        iface.addRasterLayer(self.output_path)
        return {}
    
    def name(self):
        return 'Bias correction'
    
    def shortHelpString(self):
        return "This algorithm aim at correcting both systematic elevation errors and spatially-structured random errors."

    def createInstance(self):
        return BiasCorrection()
