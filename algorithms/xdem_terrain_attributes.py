import xdem
import os

from .xdem_tools import XdemProcessingAlgorithm, dem_info

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFolderDestination)


ATTRIBUTES = {'Slope':'slope',
              'Aspect':'aspect',
              'Hillshade':'hillshade',
              'Curvature':'curvature',
              'Profile curvature':'profile_curvature',
              'Tangential curvature':'tangential_curvature',
              'Planform curvature':'planform_curvature',
              'Flowline curvature':'flowline_curvature',
              'Max curvature':'max_curvature',
              'Min curvature':'min_curvature',
              'Topographic position index':'topographic_position_index',
              'Terrain ruggedness index':'terrain_ruggedness_index',
              'Roughness':'roughness',
              'Rugosity':'rugosity',
              'Fractal roughness':'fractal_roughness',
              'Texture shading':'texture_shading'}


class TerrainAttributes(XdemProcessingAlgorithm):

    def tags(self):
        return ATTRIBUTES

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM',
            description='DEM'))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='ATTRIBUTES',
            description='Terrain attributes',
            options=ATTRIBUTES,
            defaultValue=['Slope', 'Aspect', 'Hillshade'],
            allowMultiple=True,
            usesStaticStrings=True))
        
        parameter = QgsProcessingParameterEnum(
            name='UNIT',
            description='Unit - [Slope, Aspect]',
            options=["degrees", "radians"],
            defaultValue="degrees",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name='SURFACE_FIT',
            description='Surface fit - [Slope, Aspect, Hillshade, Curvatures]',
            options=["Horn", "ZevenbergThorne", "Florinsky"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name='CURV_METHOD',
            description='Curv method - [Curvatures]',
            options=["geometric", "directional"],
            defaultValue="geometric",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='HILLSHADE_ALT',
            description='Altitude - [Hillshade] ',
            defaultValue=45)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='HILLSHADE_AZ',
            description='Azimuth - [Hillshade]',
            defaultValue=315)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='HILLSHADE_ZF',
            description='Z factor - [Hillshade]',
            defaultValue=1)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)
        
        self.addParameter(QgsProcessingParameterFolderDestination(
            name='OUTPUTS',
            description='Terrain attributes folder'))
    
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, 'DEM', context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        attributes_names= self.parameterAsStrings(parameters, 'ATTRIBUTES', context)
        
        attributes_list=[]
        for attribute_name in attributes_names:
            attributes_list.append(ATTRIBUTES[attribute_name])

        degrees=True if self.parameterAsString(parameters, 'UNIT', context)=='degrees' else False
        surface_fit = self.parameterAsString(parameters, 'SURFACE_FIT', context)
        curv_method = self.parameterAsString(parameters, 'CURV_METHOD', context)
        hillshade_altitude = self.parameterAsDouble(parameters, 'HILLSHADE_ALT', context)
        hillshade_azimuth = self.parameterAsDouble(parameters, 'HILLSHADE_AZ', context)
        hillshade_z_factor = self.parameterAsDouble(parameters, 'HILLSHADE_ZF', context)

        self.output_path = self.parameterAsString(parameters, 'OUTPUTS', context)
        os.makedirs(self.output_path, exist_ok=True)

        dem = xdem.DEM(dem_path)
        dem_info(dem, feedback)

        attributes = dem.get_terrain_attribute(attribute=attributes_list,
                                               degrees=degrees,
                                               surface_fit=surface_fit,
                                               curv_method=curv_method,
                                               hillshade_altitude=hillshade_altitude,
                                               hillshade_azimuth=hillshade_azimuth,
                                               hillshade_z_factor=hillshade_z_factor)

        if len(attributes_list) == 1:
            attributes=[attributes]

        for name, res in zip(attributes_names, attributes):
            output = os.path.join(self.output_path, f"{name}.tif")
            res.to_file(output)
        
        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        for file in os.listdir(self.output_path):
            file_path = os.path.join(self.output_path, file)
            if file_path.endswith(".tif"):
                iface.addRasterLayer(file_path)
        return {}

    def name(self):
        return 'Terrain attributes'

    def shortHelpString(self):
        return "This algorithm enables the successive calculation a wide range of terrain attributes."
    
    def createInstance(self):
        return TerrainAttributes()
