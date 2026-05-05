## xDEM QGIS Provider, Developer Guide
This guide provide the detailed documentaton for the xDEM plugin

## Project structure
- `__init__.py` - Entry point that QGIS uses for the plugin.
- `xdem_installer.py` - First file called after initialization, it installs and manages dependency conflicts.
- `xdem_plugin.py` - Plugin's main file, which calls the xDEM provider.
- `xdem_provider.py` - Provider file that lists and calls all available algorithms.
- `algorithms` - Contains the processing algorithms.
- `doc` - Contains the documentation.
- `examples` - Contains the example files, which are also used for testing
- `img` - Contains the xdem logo.
- `tests` - Contains the tests, written using the pytest framework.
- `metadata.txt` - File that allows QGIS to access the plugin's metadata and display it directly on the home page.
- `README.md` -  General project informations.

## Developement environment
As a developer, it is recommended that you use `git clone` to install the plugin. 

Here are the steps:
1. Locate the `plugins` directory where QGIS stores its installed plugins, corresponding to your current profile.
    - Go to `Settings` -> `User profiles` -> `Open active profile folder`, from there, go to `python` -> `plugins`.
2. Use `git clone` to install the xDEM plugin.
3. Restart QGIS.
4. Open the plugins menu and check the box to enable xDEM.

It will take a few minutes for the dependencies to install properly. A message confirming successful installation should appear.

A plugin that will be very useful during development is [Plugin Reloader](https://plugins.qgis.org/plugins/plugin_reloader/). By default, when changes are made to the plugin code, QGIS must be restarted. This extension allows plugins to be refreshed without closing the software.

## Tests
The tests need to be run directly from QGIS, pytest is included in the libraries installed with the plugin.

To run the tests, go to the console, import pytest and run the following command by specifying the plugin directory.
```python
import pytest

pytest.main(["plugin_directory/tests","-v"])
```
The tests will run just like a standard pytest execution, with progress updates and a final summary.

## Process algorithms
Processing methods are divided into four categories, it's all in the `algorithms` folder. Each of these categories is represented by a file.
- `xdem_corrections`- It includes coregistration, bias correction, and gap filling.
- `xdem_terrain_attributes`- It includes all the terrain attributes.
- `xdem_tools`- It includes the main class of algorithms as well as generic functions.
- `xdem_uncertainty`- It includes heteroscedasticity.
- `xdem_workflows`- It includes accuracy and topo workflows.

### QGIS Processing logic
Before getting into the logic behind xDEM processing, it is important to understand how QGIS works.

### xDEM Processing logic