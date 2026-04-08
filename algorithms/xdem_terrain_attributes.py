import xdem
import os

from .xdem_tools import dem_info

from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFolderDestination)


# Terrain Attributes

ATTRIBUTES = ['slope',
              'aspect',
              'hillshade',
              'curvature',
              'profile_curvature',
              'tangential_curvature',
              'planform_curvature',
              'flowline_curvature',
              'max_curvature',
              'min_curvature',
              'topographic_position_index',
              'terrain_ruggedness_index',
              'roughness',
              'rugosity',
              'fractal_roughness',
              'texture_shading']

class TerrainAttributes(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT_DEM', description='DEM'))
        self.addParameter(QgsProcessingParameterEnum(name='ATTRIBUTES_LIST',
                                                     description='Terrain attributes',
                                                     options=ATTRIBUTES,
                                                     defaultValue=ATTRIBUTES[0],
                                                     allowMultiple=True,
                                                     usesStaticStrings=True))
        
        parameter = QgsProcessingParameterEnum(name='UNIT',
                                              description='Unit',
                                              options=["degrees", "radians"],
                                              defaultValue="degrees",
                                              usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(name='SURFACE_FIT',
                                              description='Surface fit',
                                              options=["Horn", "ZevenbergThorne", "Florinsky"],
                                              defaultValue="Florinsky",
                                              usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(name='CURV_METHOD',
                                              description='Curv method',
                                              options=["geometric", "directional"],
                                              defaultValue="geometric",
                                              usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(name='HILLSHADE_ALT',
                                              description='Hillshade altitude',
                                              defaultValue=45)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(name='HILLSHADE_AZ',
                                              description='Hillshade azimuth',
                                              defaultValue=315)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(name='HILLSHADE_ZF',
                                              description='Hillshade Z factor',
                                              defaultValue=1)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addParameter(QgsProcessingParameterFolderDestination(name='OUTPUTS', description='Terrain attributes folder'))
    
    def processAlgorithm(self, parameters, context, feedback):
        dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT_DEM', context=context)).source()
        attributes_list = self.parameterAsStrings(parameters=parameters, name='ATTRIBUTES_LIST', context=context)

        degrees=True if self.parameterAsString(parameters=parameters, name='UNIT', context=context)=='degrees' else False
        surface_fit = self.parameterAsString(parameters=parameters, name='SURFACE_FIT', context=context)
        curv_method = self.parameterAsString(parameters=parameters, name='CURV_METHOD', context=context)
        hillshade_altitude = self.parameterAsDouble(parameters=parameters, name='HILLSHADE_ALT', context=context)
        hillshade_azimuth = self.parameterAsDouble(parameters=parameters, name='HILLSHADE_AZ', context=context)
        hillshade_z_factor = self.parameterAsDouble(parameters=parameters, name='HILLSHADE_ZF', context=context)

        self.output_path = self.parameterAsString(parameters=parameters, name='OUTPUTS', context=context)
        os.makedirs(self.output_path, exist_ok=True) # for temporary folder

        dem = xdem.DEM(dem_path)
        dem_info(dem=dem, feedback=feedback)

        attributes = dem.get_terrain_attribute(attribute=attributes_list,
                                               degrees=degrees,
                                               surface_fit=surface_fit,
                                               curv_method=curv_method,
                                               hillshade_altitude=hillshade_altitude,
                                               hillshade_azimuth=hillshade_azimuth,
                                               hillshade_z_factor=hillshade_z_factor)

        if len(attributes_list) == 1:
            attributes=[attributes]

        for name, res in zip(attributes_list, attributes):
            output = os.path.join(self.output_path, f"{name}.tif")
            res.to_file(output)
        
        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        for file in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path, file)
            if file_path.endswith(".tif"):
                iface.addRasterLayer(file_path)
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
        return 'Terrain attributes'
    
    def createInstance(self):
        return TerrainAttributes()
