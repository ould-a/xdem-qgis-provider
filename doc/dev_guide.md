## xDEM QGIS Provider, Developer Guide
This guide provide the detailed documentaton for the xDEM plugin

## Project Structure

## Devlopement environment

### Step 1: Locating the plugins directory
You must first locate the specific directory where QGIS stores its installed plugins corresponding to your current profile.

1. To access this folder in the most efficient way, install another plugin from QGIS, such as qpip (which lets you check the installed packages).
2. Once qpip is installed, click on `Installed Version`. The qpip folder will open.
3. Now, use `git clone` to install the xdem plugin into the upper directory named `plugins`.
4. Restart QGIS.
5. Open the plugins menu and check the box to enable xdem.

It will take a few minutes for the dependencies to install properly. A message confirming successful installation should appear.

One last thing before starting development, by default, when changes are made to the plugin code, QGIS must be restarted. To avoid this, install the Plugin Reloader extension, this allows the plugin to be refreshed.

## Tests
Tests can be run directly from the QGIS console. To do this, import pytest and run the following command in the plugin's test directory.
```python
import pytest
pytest.main(["plugin_directory/tests","-v"])
```
