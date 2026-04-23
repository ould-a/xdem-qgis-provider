import xdem
import os

from .xdem_tools import XdemProcessingAlgorithm
from xdem.terrain.terrain import available_attributes

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterFolderDestination)

ATTRIBUTES = available_attributes

class GetTerrainAttributes(XdemProcessingAlgorithm):

    def tags(self):
        return ATTRIBUTES

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="DEM",
            description="DEM"))
        
        self.addParameter(QgsProcessingParameterEnum(
            name="ATTRIBUTES",
            description="Terrain attributes",
            options=ATTRIBUTES,
            defaultValue=["slope", "aspect", "hillshade",],
            allowMultiple=True,
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterFolderDestination(
            name="OUTPUTS",
            description="Terrain attributes folder"))
    
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsLayer(parameters, "DEM", context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        attributes_names= self.parameterAsEnumStrings(parameters, "ATTRIBUTES", context)

        self.output_path = self.parameterAsString(parameters, "OUTPUTS", context)
        os.makedirs(self.output_path, exist_ok=True)

        dem = xdem.DEM(dem_path)

        attributes = dem.get_terrain_attribute(attribute=attributes_names)

        if len(attributes_names) == 1:
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
        return "Get terrain attributes"
    
    def groupId(self):
        return "Terrain attributes"

    def shortHelpString(self):
        return "This algorithm enables the successive calculation a wide range of terrain attributes."
    
    def createInstance(self):
        return GetTerrainAttributes()


class TerrainAttributes(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="DEM",
            description="DEM"))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name="OUTPUT",
            description=self.name()))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, "DEM", context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        output_path = self.parameterAsOutputLayer(parameters, "OUTPUT", context)

        dem = xdem.DEM(dem_path)
        attribute = self.compute_attr(dem, parameters, context)
        attribute.to_file(output_path)

        return {"OUTPUT": output_path}
    
    def groupId(self):
        return "Terrain attributes"


class Slope(TerrainAttributes):

    def initAlgorithm(self, config=None):
        super().initAlgorithm()

        parameter = QgsProcessingParameterEnum(
            name='SURFACE_FIT',
            description='Surface fit',
            options=["Horn", "ZevenbergThorne", "Florinsky"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name='UNIT',
            description='Unit',
            options=["Degrees", "Radians"],
            defaultValue="Degrees",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attr(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, 'SURFACE_FIT', context)
        degrees = True if self.parameterAsString(parameters, 'UNIT', context) == 'Degrees' else False
        slope = dem.slope(surface_fit=surface_fit, degrees=degrees)
        return slope
    
    def name(self):
        return "Slope"
    
    def createInstance(self):
        return Slope()


class Aspect(TerrainAttributes):

    def initAlgorithm(self, config=None):
        super().initAlgorithm()

        parameter = QgsProcessingParameterEnum(
            name='SURFACE_FIT',
            description='Surface fit',
            options=["Horn", "ZevenbergThorne", "Florinsky"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name='UNIT',
            description='Unit',
            options=["Degrees", "Radians"],
            defaultValue="Degrees",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attr(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, 'SURFACE_FIT', context)
        degrees = True if self.parameterAsString(parameters, 'UNIT', context) == 'Degrees' else False
        aspect = dem.aspect(surface_fit=surface_fit, degrees=degrees)
        return aspect
    
    def name(self):
        return "Aspect"
    
    def createInstance(self):
        return Aspect()
    

class Hillshade(TerrainAttributes):

    def initAlgorithm(self, config=None):
        super().initAlgorithm()

        parameter = QgsProcessingParameterEnum(
            name='SURFACE_FIT',
            description='Surface fit',
            options=["Horn", "ZevenbergThorne", "Florinsky"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='ALTITUDE',
            description='Altitude',
            defaultValue=45)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='AZIMUTH',
            description='Azimuth',
            defaultValue=315)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name='ZFACTOR',
            description='Z factor',
            defaultValue=1)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attr(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, 'SURFACE_FIT', context)
        altitude = self.parameterAsDouble(parameters, 'ALTITUDE', context)
        azimuth = self.parameterAsDouble(parameters, 'AZIMUTH', context)
        z_factor = self.parameterAsDouble(parameters, 'ZFACTOR', context)
        hillshade = dem.hillshade(surface_fit=surface_fit, azimuth=azimuth, altitude=altitude, z_factor=z_factor)
        return hillshade
    
    def name(self):
        return "Hillshade"
    
    def createInstance(self):
        return Hillshade()