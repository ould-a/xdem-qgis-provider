import xdem
import os
import geoutils as gu

from .xdem_tools import *

from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterFolderDestination)


# Coregistration

COREG_METHODS = ['Nuth and Kaab (2011)',
                 'Minimization of dh',
                 'Least Z-difference',
                 'Iterative closest point',
                 'Coherent point drift',
                 'Vertical shift']

class Coregistration(QgsProcessingAlgorithm):
    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
    
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_TBA_DEM', description='Tba DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_REF_DEM', description='Ref DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_INLIER_MASK', description='Inlier mask', defaultValue=None, optional=True))
        self.addParameter(QgsProcessingParameterEnum(name='COREG_METHOD',
                                                     description='Method',
                                                     options=COREG_METHODS,
                                                     defaultValue=COREG_METHODS[2],
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
    
    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)
    
    def name(self):
        return 'Coregistration'

    def createInstance(self):
        return Coregistration()
