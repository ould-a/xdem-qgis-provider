import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterRasterDestination)


COREGISTRATION_METHODS = ['Nuth and Kaab (2011)',
                 'Minimization of dh',
                 'Least Z-difference',
                 'Iterative closest point',
                 'Coherent point drift',
                 'Vertical shift']


class Coregistration(XdemProcessingAlgorithm):

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
            options=COREGISTRATION_METHODS,
            defaultValue=COREGISTRATION_METHODS[0],
            usesStaticStrings=True))

        parameter = QgsProcessingParameterNumber(
            name='BLOCKSIZE_FIT',
            description='Block size fit')
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='BLOCKSIZE_APPLY',
            description='Block size apply')
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addParameter(QgsProcessingParameterRasterDestination(
            name='OUTPUT',
            description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_path = (self.parameterAsRasterLayer(parameters, 'DEM_1', context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'DEM_2', context)).source()

        method = self.parameterAsString(parameters, 'METHOD', context)
        block_size_fit = self.parameterAsInt(parameters, 'BLOCKSIZE_FIT', context)
        block_size_apply = self.parameterAsInt(parameters, 'BLOCKSIZE_APPLY', context)

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

        if method == 'Nuth and Kaab (2011)':
            coreg = xdem.coreg.NuthKaab()

        elif method == 'Minimization of dh':
            coreg = xdem.coreg.DhMinimize()

        elif method == 'Least Z-difference':
            coreg = xdem.coreg.LZD()

        elif method == 'Iterative closest point':
            coreg = xdem.coreg.ICP()

        elif method == 'Coherent point drift':
            coreg = xdem.coreg.CPD()

        elif method == 'Vertical shift':
            coreg = xdem.coreg.VerticalShift()

        if block_size_fit != 0 and block_size_apply != 0:
            coreg = xdem.coreg.BlockwiseCoreg(coreg,
                                            block_size_fit=block_size_fit,
                                            block_size_apply=block_size_apply,
                                            parent_path="")
            coreg.fit(ref_dem, tba_dem, inlier_mask)
            aligned_dem = coreg.apply()

        else :
            coreg.fit(ref_dem, tba_dem, inlier_mask)
            aligned_dem = coreg.apply(tba_dem)
            coreg_info(coreg, feedback)

        aligned_dem.to_file(self.output_path)

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        iface.addRasterLayer(self.output_path)
        return {}
    
    def name(self):
        return 'Coregistration'
    
    def shortHelpString(self):
        return "This algorithm enables the coregistration by applying affine methods."

    def createInstance(self):
        return Coregistration()
