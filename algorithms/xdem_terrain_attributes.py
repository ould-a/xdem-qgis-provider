import xdem
import os

from .xdem_tools import XdemProcessingAlgorithm
from xdem.terrain.terrain import available_attributes

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
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
        dem_path = (self.parameterAsLayer(parameters, "DEM", context)).source()
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
