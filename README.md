## xDEM QGIS Provider

This plugin allows you to perform processing on Digital Elevation Models (DEMs), it is based on the xDEM Python package. A package developed in collaboration between CNES (the French space agency) and Glacio Hack (a group of glaciology researchers).

### Installation
You can install the plugin directly within QGIS:
1. Go to `Plugins > Manage and Install Plugins`.
2. Search for "xDEM Provider".
3. Click `Install Plugin`,

Installing the dependencies may take a few minutes, do not force QGIS to close.

### Available processing
All the algorithms can be accessed through the QGIS Processing Toolbox in `xDEM`, they are organized into four sections.
- **Corections**: For coregistration, bias corrections and gap filling
- **Terrain attributes**: To calculate derivatives of DEMs, such as curvature
- **Uncertainty**: To identify potential errors resulting from coregistration
- **Workflows**: To run full pipelines that generate detailed reports

### Documentation
- [xDEM package](https://xdem.readthedocs.io/en/stable/index.html)
- [Developper guide](dev/README.md)

### Licence

### Citation