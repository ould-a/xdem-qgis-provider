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


# Uncertainty analysis

class Uncertainty(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_COREG_DEM', description='Coreg DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_REF_DEM', description='Ref DEM'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='STABLE_TERRAIN_MASK', description='Stable terrain mask'))
        self.addParameter(QgsProcessingParameterRasterDestination(name='OUTPUT', description='Map of variable errors'))
    
    def processAlgorithm(self, parameters, context, feedback):
        coreg_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_COREG_DEM', context=context)).source()
        ref_dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_REF_DEM', context=context)).source()
        stabe_terrain_path = (self.parameterAsRasterLayer(parameters=parameters, name='STABLE_TERRAIN_MASK', context=context)).source()
        self.output_path = self.parameterAsString(parameters=parameters, name='OUTPUT', context=context)

        coreg_dem = xdem.DEM(coreg_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)
        stabe_terrain = gu.Raster(stabe_terrain_path, is_mask=True)

        sig_dem = coreg_dem.estimate_uncertainty(ref_dem, stable_terrain=stabe_terrain, precision_of_other="same")

        sig_dem.to_file(self.output_path)
        
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
        return 'Uncertainty analysis'
    
    def createInstance(self):
        return Uncertainty()