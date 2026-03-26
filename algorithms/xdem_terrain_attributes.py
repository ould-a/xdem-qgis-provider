import xdem

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


# Terrain Attributes

class TerrainAttributes(QgsProcessingAlgorithm):
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

class Slope(TerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.slope())

    def name(self):
        return 'Slope'
    
    def createInstance(self):
        return Slope()
    
class Aspect(TerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.aspect())

    def name(self):
        return 'Aspect'
    
    def createInstance(self):
        return Aspect()

class Hillshade(TerrainAttributes):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_terrain_attributes(parameters=parameters, context=context, feedback=feedback, terrain_attribute=lambda x: x.hillshade())

    def name(self):
        return 'Hillshade'
    
    def createInstance(self):
        return Hillshade()
