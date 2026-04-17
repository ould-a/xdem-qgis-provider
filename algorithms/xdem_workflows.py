import xdem
import os

from xdem.workflows import Topo
from xdem.workflows.schemas import STATS_METHODS, TERRAIN_ATTRIBUTES
from .xdem_tools import XdemProcessingAlgorithm
from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFolderDestination)


class TopoWorkflow(XdemProcessingAlgorithm):

    def tags(self):
        return TERRAIN_ATTRIBUTES

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name='DEM',
            description='DEM'))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='ATTRIBUTES',
            description='Terrain attributes',
            options=TERRAIN_ATTRIBUTES,
            defaultValue=['slope', 'aspect', 'hillshade', "profile_curvature"],
            allowMultiple=True,
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterEnum(
            name='STATS',
            description='Statistics',
            options=STATS_METHODS,
            defaultValue=['min', 'max', 'mean', 'median', "nmad"],
            allowMultiple=True,
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterFolderDestination(
            name='OUTPUT',
            description='Topographical summary folder'))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, 'DEM', context)
        dem_path = dem_layer.dataProvider().dataSourceUri()

        attributes= self.parameterAsEnumStrings(parameters, 'ATTRIBUTES', context)
        if len(attributes) == 1:
            feedback.pushWarning("You must provide at least two attributes")
            return {}

        stats= self.parameterAsEnumStrings(parameters, 'STATS', context)
        if len(stats) == 1:
            feedback.pushWarning("You must provide at least two statitics")
            return {}

        self.output_path = self.parameterAsString(parameters, 'OUTPUT', context)
        os.makedirs(self.output_path, exist_ok=True)

        config = {
            "inputs": {
                "reference_elev": {
                    "path_to_elev": dem_path,
                    "force_source_nodata": None,
                    "from_vcrs": None,
                    "to_vcrs": None,
                    "path_to_mask": None,
                    "downsample": 1,
                },
            },
            "outputs": {"level": 2, "path": str(self.output_path)},
            "statistics": stats,
            "terrain_attributes": attributes,
        }

        workflows = Topo(config)
        workflows.run()

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        rasters_file = os.path.join(self.output_path, "rasters")
        for file in os.listdir(rasters_file):
            file_path = os.path.join(rasters_file, file)
            iface.addRasterLayer(file_path)
        return {}

    def name(self):
        return 'Topography'

    def shortHelpString(self):
        return "The topo workflow of performs a topographical summary of an elevation dataset.\n" \
        "This summary derives a series of terrain attributes (e.g. slope, hillshade, aspect, etc.) with statistics (e.g. mean, max, min, etc.)."

    def createInstance(self):
        return TopoWorkflow()
