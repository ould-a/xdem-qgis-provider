# xDEM QGIS Provider, Developer Guide
This guide provide the detailed documentaton for developers.

## Project structure
- `__init__.py` - Entry point that QGIS uses for the plugin.
- `xdem_installer.py` - First file called in initialization, it installs and manages dependency conflicts.
- `xdem_plugin.py` - Plugin's main file, which calls the xDEM provider.
- `xdem_provider.py` - Provider file that lists and calls all available algorithms.
- `algorithms` - Contains the processing algorithms.
- `doc` - Contains the documentation.
- `examples` - Contains the example files, which are also used for testing
- `img` - Contains the xdem logo.
- `tests` - Contains the tests, written using the pytest framework.
- `metadata.txt` - File containing metadata, displayed directly on the home page.
- `README.md` -  General project informations.

## Developement environment
For developers, it is recommended to use `git clone` to install the plugin. 

Here are the steps:
1. Locate the `plugins` directory where QGIS stores its installed plugins, corresponding to your current profile.
    - Go to `Settings` > `User profiles` > `Open active profile folder`, from there, go to `python` > `plugins`.
2. Use `git clone https://github.com/ould-a/xdem-qgis-provider.git` to install the xDEM plugin.
3. Restart QGIS.
4. Open the plugins menu and check the box to enable xDEM.

It will take a few minutes for the dependencies to install properly. A message confirming successful installation should appear.

A plugin that will be very helpful during development is [Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/). By default, when changes are made to the plugin code, QGIS must be restarted. This extension allows plugins to be refreshed without closing the software.

## Tests
The tests need to be run directly from QGIS, pytest is included in the libraries installed with the plugin.

To run the tests, go to the console, import pytest and run the following command by specifying the plugin directory.
```python
import pytest

pytest.main(["plugin_directory/tests", "-v"])
```
The tests will run just like a standard pytest execution, with progress updates and a final summary.

## Process algorithms
Processing methods are divided into four categories, it's all in the `algorithms` folder. Each of these categories is represented by a file.
- `xdem_tools`- It includes the main class of algorithms as well as generic functions.
- `xdem_corrections`- It includes coregistration, bias correction, and gap filling.
- `xdem_terrain_attributes`- It includes all the terrain attributes.
- `xdem_uncertainty`- It includes heteroscedasticity.
- `xdem_workflows`- It includes accuracy and topo workflows.

#### QGIS Processing logic
Before getting into the logic behind xDEM processing, it is important to understand how QGIS process algorithms works.

Every processing must inherit from the class `QgsProcessingAlgorithm`, it is the main processing class.

The two most important methods are:
1. `initAlgorithm()` this method initialize the GUI, it explicitly specifies which parameters need to be entered for the algorithm to work.
2. `processAlgorithm()` this method retrieves the parameters provided by the user and runs the process.

#### xDEM Processing logic
The xdem algorithms follow this logic. Here is a simplified version of a slope processing:
```
class Slope(QgsProcessingAlgorithm):
    def initAlgorithm()
        # Input DEM
        self.addParameter(QgsProcessingParameterRasterLayer(name="INPUT", description="Dem"))

        # Output Slope
        self.addParameter(QgsProcessingParameterRasterDestination(name="OUTPUT", description="Slope"))

    def processAlgorithm(parameters)
        # Loading the layer from QGIS
        dem_layer = self.parameterAsRasterLayer(parameters, "INPUT")

        # Getting the slope output directory
        output_path = self.parameterAsOutputLayer(parameters, "OUTPUT")

        # Extracting the layer path
        dem_path = dem_layer.dataProvider().dataSourceUri()

        # Convert to a DEM object
        dem = xdem.DEM(dem_path)

        # Compute the slope
        slope = dem.slope()

        # Saving it
        slope.to_file(output_path)

        # Return the result in QGIS
        return {"OUTPUT": output_path}
```
