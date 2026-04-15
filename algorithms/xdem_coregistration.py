import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination)


METHODS = {'Nuth and Kääb (2011)': xdem.coreg.NuthKaab(),
           'Minimization of dh': xdem.coreg.DhMinimize(),
           'Least Z-difference': xdem.coreg.LZD(),
           'Iterative closest point': xdem.coreg.ICP(),
           'Coherent point drift': xdem.coreg.CPD(),
           'Vertical shift': xdem.coreg.VerticalShift()}


class Coregistration(XdemProcessingAlgorithm):

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
            defaultValue='Nuth and Kääb (2011)',
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
        return 'Coregistration'
    
    def shortHelpString(self):
        return "This algorithm enables the coregistration of two DEMs by applying affine methods."

    def createInstance(self):
        return Coregistration()
