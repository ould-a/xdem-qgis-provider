import xdem
import os

from .xdem_tools import dem_info

from qgis.PyQt.QtCore import QCoreApplication
from qgis.utils import iface
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterRasterDestination,
                       QgsProcessingParameterFolderDestination)


# Terrain Attributes

ATTRIBUTES = ['Slope',
              'Aspect',
              'Hillshade',
              'Profile curvature',
              'Terrain ruggedness index',
              'Rugosity']

class TerrainAttributes(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT', description='DEM'))
        self.addParameter(QgsProcessingParameterEnum(name='ATTRIBUTE',
                                                     description='Terrain attributes',
                                                     options=ATTRIBUTES,
                                                     defaultValue=ATTRIBUTES[0],
                                                     allowMultiple=True))

        # Advanced Parameters
        # Slope
        parameter= QgsProcessingParameterEnum(name='SLOPEUNIT',
                                              description='[Slope] Unit',
                                              options=['degrees', 'radians'],
                                              defaultValue='degrees',
                                              usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter= QgsProcessingParameterEnum(name='SLOPEMETHOD',
                                              description='[Slope] Method',
                                              options=['Horn', 'ZevenbergThorne', 'Florinsky'],
                                              defaultValue='Florinsky',
                                              usesStaticStrings=True)
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        self.addParameter(QgsProcessingParameterFolderDestination(name='OUTPUTS', description='Terrain attributes folder'))
    
    def processAlgorithm(self, parameters, context, feedback):
        dem_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT', context=context)).source()
        attribute_parameters = self.parameterAsEnums(parameters=parameters, name='ATTRIBUTE', context=context)

        slope_unit = self.parameterAsString(parameters=parameters, name='SLOPEUNIT', context=context)
        slope_method = self.parameterAsString(parameters=parameters, name='SLOPEMETHOD', context=context)

        self.output_path = self.parameterAsString(parameters=parameters, name='OUTPUTS', context=context)
        os.makedirs(self.output_path, exist_ok=True) # for temporary folder

        dem = xdem.DEM(dem_path)
        dem_info(dem=dem, feedback=feedback)

        for i in attribute_parameters:
            attr = ATTRIBUTES[i]

            if attr == 'Slope':
                deg = True
                if slope_unit == 'radians': deg = False
                terrain_attribute = dem.slope(surface_fit=slope_method, degrees=deg)

            elif attr == 'Aspect':
                terrain_attribute = dem.aspect()

            elif attr == 'Hillshade':
                terrain_attribute = dem.hillshade()

            elif attr == 'Profile cuvature':
                terrain_attribute = dem.profile_curvature()

            elif attr == 'Terrain ruggedness index':
                terrain_attribute = dem.terrain_ruggedness_index()
                
            elif attr == 'Rugosity':
                terrain_attribute = dem.rugosity()
            
            terrain_attribute.to_file(os.path.join(self.output_path, f"{attr}.tif"))
        
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


# Old version

class OldTerrainAttributes(QgsProcessingAlgorithm):
    """
    Generic terrain attributes class, with a DEM as input and an output file for the attribute.
    """

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT', self.tr('DEM')))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT', self.tr(self.name())))
    
    def run_terrain_attributes(self, parameters, context, feedback, terrain_attribute):
        """
        Function to load a DEM, apply the specified terrain attribute and save it.
        """

        dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT', context)).source()
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        dem = xdem.DEM(dem_path)

        result = terrain_attribute(dem)
        
        result.to_file(output_path)
        return {'OUTPUT' : output_path}

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Terrain attributes'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

class Slope(OldTerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.slope())

    def name(self):
        return 'Slope'
    
    def createInstance(self):
        return Slope()
    
class Aspect(OldTerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.aspect())

    def name(self):
        return 'Aspect'
    
    def createInstance(self):
        return Aspect()

class Hillshade(OldTerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.hillshade())

    def name(self):
        return 'Hillshade'
    
    def createInstance(self):
        return Hillshade()
