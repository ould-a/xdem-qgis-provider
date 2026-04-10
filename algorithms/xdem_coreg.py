import xdem
import geoutils as gu

from .xdem_tools import XdemProcessingAlgorithm, coreg_info

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterRasterDestination)


COREGISTRATION_METHODS = ['Nuth and Kaab (2011)',
                 'Minimization of dh',
                 'Least Z-difference',
                 'Iterative closest point',
                 'Coherent point drift',
                 'Vertical shift']

BIAS_CORRECTION_METHODS = ['Deramping',
                           'Directional biases',
                           'Terrain biases']


class Coregistration(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_TBA_DEM', description='Tba DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_REF_DEM', description='Ref DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_INLIER_MASK', description='Inlier mask', defaultValue=None, optional=True))
        self.addParameter(QgsProcessingParameterEnum(name='COREG_METHOD',
                                                     description='Method',
                                                     options=COREGISTRATION_METHODS,
                                                     defaultValue=COREGISTRATION_METHODS[0],
                                                     usesStaticStrings=True))
        
        parameter= QgsProcessingParameterBoolean(name='BLOCKWISE', description='Blockwise', defaultValue=False)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(name='BLOCKSIZE_FIT', description='Block size fit', defaultValue=500)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(name='BLOCKSIZE_APPLY', description='Block size apply', defaultValue=1000)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addParameter(QgsProcessingParameterRasterDestination(name='OUTPUT', description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_TBA_DEM', context=context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_REF_DEM', context=context)).source()
        method = self.parameterAsString(parameters=parameters, name='COREG_METHOD', context=context)

        block_size_fit = self.parameterAsInt(parameters=parameters, name='BLOCKSIZE_FIT', context=context)
        block_size_apply = self.parameterAsInt(parameters=parameters, name='BLOCKSIZE_APPLY', context=context)
        blockwise = self.parameterAsBoolean(parameters=parameters, name='BLOCKWISE', context=context)

        self.output_path = self.parameterAsOutputLayer(parameters=parameters, name='OUTPUT', context=context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = None

        try:
            inlier_mask_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_INLIER_MASK', context=context)).source()
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

        if blockwise :
            if coreg.is_affine == True:
                coreg = xdem.coreg.BlockwiseCoreg(coreg, block_size_fit=block_size_fit, block_size_apply=block_size_apply, parent_path="")
                coreg.fit(ref_dem, tba_dem, inlier_mask)
                aligned_dem = coreg.apply()
        else :
            coreg.fit(ref_dem, tba_dem, inlier_mask)
            aligned_dem = coreg.apply(tba_dem)
            coreg_info(coreg=coreg, feedback=feedback)

        aligned_dem.to_file(self.output_path)

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        iface.addRasterLayer(self.output_path)
        return {}
    
    def name(self):
        return 'Coregistration'

    def createInstance(self):
        return Coregistration()


class BiasCorrection(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_TBA_DEM', description='Tba DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_REF_DEM', description='Ref DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_INLIER_MASK', description='Inlier mask', defaultValue=None, optional=True))
        self.addParameter(QgsProcessingParameterEnum(name='BIAS_CORR_METHOD',
                                                     description='Method',
                                                     options=BIAS_CORRECTION_METHODS,
                                                     defaultValue=BIAS_CORRECTION_METHODS[0],
                                                     usesStaticStrings=True))

        self.addParameter(QgsProcessingParameterRasterDestination(name='OUTPUT', description='Aligned DEM'))

    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_TBA_DEM', context=context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_REF_DEM', context=context)).source()
        method = self.parameterAsString(parameters=parameters, name='BIAS_CORR_METHOD', context=context)

        self.output_path = self.parameterAsOutputLayer(parameters=parameters, name='OUTPUT', context=context)

        tba_dem = xdem.DEM(tba_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)

        inlier_mask = None

        try:
            inlier_mask_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_INLIER_MASK', context=context)).source()
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

        sig_dem, rho_sig = aligned_dem.estimate_uncertainty(ref_dem, stable_terrain = inlier_mask)

        sig_dem.to_file(self.output_path)

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        iface.addRasterLayer(self.output_path)
        return {}
    
    def name(self):
        return 'Bias correction'

    def createInstance(self):
        return BiasCorrection()
