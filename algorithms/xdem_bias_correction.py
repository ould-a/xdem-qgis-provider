import xdem

from .xdem_tools import XdemProcessingAlgorithm, coreg_info, load_mask
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterMapLayer,
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
            name='TBA_DEM',
            description='DEM to be aligned'))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='REF_DEM',
            description='Reference DEM'))
        
        self.addParameter(QgsProcessingParameterMapLayer(
            name='MASK',
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
        tba_dem_layer = self.parameterAsRasterLayer(parameters, 'TBA_DEM', context)
        ref_dem_layer = self.parameterAsRasterLayer(parameters, 'REF_DEM', context)
        tba_dem_path = tba_dem_layer.dataProvider().dataSourceUri()
        ref_dem_path = ref_dem_layer.dataProvider().dataSourceUri()
        method = self.parameterAsString(parameters, 'METHOD', context)
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = load_mask(self, parameters, context, feedback, ref_dem)

        coreg = METHODS[method]

        coreg.fit(ref_dem, tba_dem, inlier_mask)
        aligned_dem = coreg.apply(tba_dem)
        coreg_info(coreg, feedback)

        aligned_dem.to_file(output_path)

        return {'OUTPUT': output_path}
    
    def name(self):
        return 'Bias correction'
    
    def shortHelpString(self):
        return "This algorithm aim at correcting both systematic elevation errors and spatially-structured random errors."

    def createInstance(self):
        return BiasCorrection()
