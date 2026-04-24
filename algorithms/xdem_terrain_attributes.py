import xdem

from .xdem_tools import XdemProcessingAlgorithm

from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination)


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
        attribute = self.compute_attribute(dem, parameters, context)
        attribute.to_file(output_path)

        return {"OUTPUT": output_path}
    
    def groupId(self):
        return "Terrain attributes"
        

class Slope(TerrainAttributes):

    def initAlgorithm(self, config=None):
        super().initAlgorithm()

        parameter = QgsProcessingParameterEnum(
            name="SURFACE_FIT",
            description="Surface fit",
            options=["Florinsky", "Horn", "ZevenbergThorne"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name="UNIT",
            description="Unit",
            options=["Degrees", "Radians"],
            defaultValue="Degrees",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attribute(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, "SURFACE_FIT", context)
        degrees = True if self.parameterAsString(parameters, "UNIT", context) == "Degrees" else False
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
            name="SURFACE_FIT",
            description="Surface fit",
            options=["Florinsky", "Horn", "ZevenbergThorne"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterEnum(
            name="UNIT",
            description="Unit",
            options=["Degrees", "Radians"],
            defaultValue="Degrees",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attribute(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, "SURFACE_FIT", context)
        degrees = True if self.parameterAsString(parameters, "UNIT", context) == "Degrees" else False
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
            name="SURFACE_FIT",
            description="Surface fit",
            options=["Florinsky", "Horn", "ZevenbergThorne"],
            defaultValue="Florinsky",
            usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name="ALTITUDE",
            description="Altitude",
            defaultValue=45)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name="AZIMUTH",
            description="Azimuth",
            defaultValue=315)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = QgsProcessingParameterNumber(
            name="ZFACTOR",
            description="Z factor",
            defaultValue=1)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

    def compute_attribute(self, dem, parameters, context):
        surface_fit = self.parameterAsString(parameters, "SURFACE_FIT", context)
        altitude = self.parameterAsInt(parameters, "ALTITUDE", context)
        azimuth = self.parameterAsInt(parameters, "AZIMUTH", context)
        z_factor = self.parameterAsInt(parameters, "ZFACTOR", context)
        hillshade = dem.hillshade(surface_fit=surface_fit, altitude=altitude, azimuth=azimuth, z_factor=z_factor)
        return hillshade
    
    def name(self):
        return "Hillshade"
    
    def createInstance(self):
        return Hillshade()