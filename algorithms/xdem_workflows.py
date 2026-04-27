import os

from .xdem_tools import XdemProcessingAlgorithm
from xdem.workflows import Accuracy, Topo
from xdem.workflows.schemas import STATS_METHODS, TERRAIN_ATTRIBUTES, COREG_METHODS

from qgis.utils import iface
from qgis.core import (QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterFolderDestination)


class AccuracyWorkflow(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="TBA_DEM",
            description="DEM to be aligned"))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="REF_DEM",
            description="Reference DEM"))
        
        self.addParameter(QgsProcessingParameterEnum(
            name="METHOD1",
            description="Method - 1",
            options=COREG_METHODS[:-1],
            defaultValue="NuthKaab",
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterEnum(
            name="STATS",
            description="Statistics",
            options=STATS_METHODS,
            defaultValue=["min", "max", "mean", "median", "nmad"],
            allowMultiple=True,
            usesStaticStrings=True))
        
        parameter = (QgsProcessingParameterEnum(
            name="METHOD2",
            description="Method - 2",
            options=COREG_METHODS[:-1],
            optional=True,
            usesStaticStrings=True))
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)

        parameter = (QgsProcessingParameterEnum(
            name="METHOD3",
            description="Method - 3",
            options=COREG_METHODS[:-1],
            optional=True,
            usesStaticStrings=True))
        parameter.setFlags(parameter.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(parameter)
        
        self.addParameter(QgsProcessingParameterFolderDestination(
            name="OUTPUT",
            description="Accuracy folder"))
        
    def processAlgorithm(self, parameters, context, feedback):
        tba_dem_layer = self.parameterAsRasterLayer(parameters, "TBA_DEM", context)
        ref_dem_layer = self.parameterAsRasterLayer(parameters, "REF_DEM", context)
        tba_dem_path = tba_dem_layer.dataProvider().dataSourceUri()
        ref_dem_path = ref_dem_layer.dataProvider().dataSourceUri()
        method1 = self.parameterAsString(parameters, "METHOD1", context)
        method2 = self.parameterAsString(parameters, "METHOD2", context)
        method3 = self.parameterAsString(parameters, "METHOD3", context)
        stats = self.parameterAsEnumStrings(parameters, "STATS", context)

        self.output_path = self.parameterAsString(parameters, "OUTPUT", context)
        os.makedirs(self.output_path, exist_ok=True)

        config= {
            "inputs": {
                "reference_elev": {
                    "path_to_elev": ref_dem_path,
                },
                "to_be_aligned_elev": {
                    "path_to_elev": tba_dem_path,
                },
            },
            "outputs": {
                "level": 2,
                "path": str(self.output_path),
            },
            "coregistration": {
                "step_one": {
                    "method": method1
                },
                "step_two": {
                    "method": None if method2 == "" else method2
                },
                "step_three": {
                    "method":  None if method3 == "" else method3
                },
            },
            "statistics": stats
        }

        workflow = Accuracy(config)
        workflow.run()
        try:
            from weasyprint import HTML
            HTML(workflow.outputs_folder / "report.html").write_pdf(workflow.outputs_folder / "report.pdf")
        except ImportError:
            pass

        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        rasters_folder = os.path.join(self.output_path, "rasters")
        for file in os.listdir(rasters_folder):
            file_path = os.path.join(rasters_folder, file)
            iface.addRasterLayer(file_path)
        return {}

    def name(self):
        return "Accuracy"
    
    def groupId(self):
        return "Workflows"

    def shortHelpString(self):
        return "The accuracy workflow performs an accuracy assessment of an elevation dataset.\n" \
        "This assessment relies on analyzing the elevation differences to a secondary elevation dataset on static surfaces," \
        " as an error proxy to perform coregistration and bias-correction (systematic errors) and to perform uncertainty quantification (structured random errors)."

    def createInstance(self):
        return AccuracyWorkflow()


class TopoWorkflow(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="DEM",
            description="DEM"))
        
        self.addParameter(QgsProcessingParameterEnum(
            name="ATTRIBUTES",
            description="Terrain attributes",
            options=TERRAIN_ATTRIBUTES,
            defaultValue=["slope", "aspect", "hillshade", "profile_curvature"],
            allowMultiple=True,
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterEnum(
            name="STATS",
            description="Statistics",
            options=STATS_METHODS,
            defaultValue=["min", "max", "mean", "median", "nmad"],
            allowMultiple=True,
            usesStaticStrings=True))
        
        self.addParameter(QgsProcessingParameterFolderDestination(
            name="OUTPUT",
            description="Topography folder"))
        
    def processAlgorithm(self, parameters, context, feedback):
        dem_layer = self.parameterAsRasterLayer(parameters, "DEM", context)
        dem_path = dem_layer.dataProvider().dataSourceUri()
        stats = self.parameterAsEnumStrings(parameters, "STATS", context)
        attributes = self.parameterAsEnumStrings(parameters, "ATTRIBUTES", context)

        self.output_path = self.parameterAsString(parameters, "OUTPUT", context)
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

        workflow = Topo(config)
        workflow.run()
        try:
            from weasyprint import HTML
            HTML(workflow.outputs_folder / "report.html").write_pdf(workflow.outputs_folder / "report.pdf")
        except ImportError:
            pass
        return {}
    
    def postProcessAlgorithm(self, context, feedback):
        rasters_folder = os.path.join(self.output_path, "rasters")
        for file in os.listdir(rasters_folder):
            file_path = os.path.join(rasters_folder, file)
            iface.addRasterLayer(file_path)
        return {}

    def name(self):
        return "Topography"
    
    def groupId(self):
        return "Workflows"

    def shortHelpString(self):
        return "The topo workflow performs a topographical summary of an elevation dataset.\n" \
        "This summary derives a series of terrain attributes (e.g. slope, hillshade, aspect, etc.) with statistics (e.g. mean, max, min, etc.)."

    def createInstance(self):
        return TopoWorkflow()