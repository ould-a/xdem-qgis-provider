import xdem
from .xdem_tools import XdemProcessingAlgorithm, load_mask
from qgis.core import (
    QgsProcessingParameterRasterLayer,
    QgsProcessingParameterRasterDestination
)


class Heteroscedasticity(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="AL_DEM",
            description="Aligned DEM"))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="REF_DEM",
            description="Reference DEM"))
        
        self.addParameter(QgsProcessingParameterRasterLayer(
            name="MASK",
            description="Stable terrain mask",
            defaultValue=None))
        
        self.addParameter(QgsProcessingParameterRasterDestination(
            name="OUTPUT",
            description="Map of variable error"))
        
    def processAlgorithm(self, parameters, context, feedback):
        aligned_dem_layer = self.parameterAsRasterLayer(parameters, "AL_DEM", context)
        ref_dem_layer = self.parameterAsRasterLayer(parameters, "REF_DEM", context)
        aligned_dem_path = aligned_dem_layer.dataProvider().dataSourceUri()
        ref_dem_path = ref_dem_layer.dataProvider().dataSourceUri()
        output_path = self.parameterAsOutputLayer(parameters, "OUTPUT", context)

        aligned_dem = xdem.DEM(aligned_dem_path)
        ref_dem = xdem.DEM(ref_dem_path)
        
        ddem = ref_dem - aligned_dem

        stable_terrain = load_mask(self, parameters, context, feedback, ref_dem)

        slope, max_curvature = xdem.terrain.get_terrain_attribute(ref_dem, attribute=["slope", "max_curvature"])

        errors, df_binning, error_function = xdem.spatialstats.infer_heteroscedasticity_from_stable(
        dvalues=ddem, list_var=[slope, max_curvature], list_var_names=["slope", "maxc"], stable_mask=stable_terrain)

        errors.to_file(output_path)

        return {"OUTPUT": output_path}
    
    def name(self):
        return "Heteroscedasticity"
    
    def groupId(self):
        return "Uncertainty"

    def shortHelpString(self):
        return "Digital elevation models have a precision that can vary with terrain and instrument-related variables.\n" \
        "Heteroscedasticity occurs when the variance of the errors is not constant across all values of the explanatory variables.\n" \
        "This algorithm relies on a framework of non-stationary spatial statistics to estimate and model this variability in elevation error, " \
        "using terrain slope and maximum curvature as explanatory variables, with stable terrain as an error proxy for moving terrain."

    def createInstance(self):
        return Heteroscedasticity()
