import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info, load_mask

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDefinition,
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
            defaultValue='Nuth and Kääb (2011)',
            usesStaticStrings=True))
        
        parameter = QgsProcessingParameterNumber(
            name='BLOCKSIZE',
            description='Blocksize',
            defaultValue=0)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_layer = self.parameterAsRasterLayer(parameters, 'TBA_DEM', context)
        ref_dem_layer = self.parameterAsRasterLayer(parameters, 'REF_DEM', context)
        tba_dem_path = tba_dem_layer.source()
        ref_dem_path = ref_dem_layer.source()
        method = self.parameterAsString(parameters, 'METHOD', context)
        block_size = self.parameterAsDouble(parameters, 'BLOCKSIZE', context)
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = load_mask(self, parameters, context, feedback, ref_dem)

        coreg = METHODS[method]

        if block_size != 0:
            import os
            feedback.pushWarning("Curently, Blockwise work only with Nuth and Kääb (2011)")
            blockwise = xdem.coreg.BlockwiseCoreg(xdem.coreg.NuthKaab(),
                                      block_size_fit=block_size,
                                      block_size_apply=block_size,
                                      parent_path=os.path.dirname(__file__))
            blockwise.fit(ref_dem, tba_dem, inlier_mask)
            aligned_dem = blockwise.apply()
        else:
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
