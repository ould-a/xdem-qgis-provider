import subprocess

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProject,
                       QgsRasterLayer,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)

from .xdem_config import (PY_XDEM,
                          SUBPROCESS_SCRIPT)


def _add_to_project(output_path, algorithm):
    layer = QgsRasterLayer(output_path, algorithm)
    QgsProject.instance().addMapLayer(layer)
    return {'OUTPUT' : output_path}


# Terrain attributes

class TerrainAttributes(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT1', self.tr('DEM')))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT', self.tr('Output')))

    def processAlgorithm(self, parameters, context, feedback):
        dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT1', context)).source()
        output_path = self.parameterAsFileOutput(parameters, 'OUTPUT', context)
        algorithm = self.name()
        subprocess.run([PY_XDEM, SUBPROCESS_SCRIPT, algorithm, dem_path, "", output_path], check=True)
        return _add_to_project(output_path=output_path, algorithm=algorithm)

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Terrain attributes'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

class Aspect(TerrainAttributes):
    def name(self):
        return 'Aspect'
    def createInstance(self):
        return Aspect()

class Hillshade(TerrainAttributes):
    def name(self):
        return 'Hillshade'
    def createInstance(self):
        return Hillshade()

class Slope(TerrainAttributes):
    def name(self):
        return 'Slope'
    def createInstance(self):
        return Slope()


# Coregistration

class Coregistration(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT1', self.tr('Ref DEM')))
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT2', self.tr('Tba DEM')))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT', self.tr('Aligned DEM')))

    def processAlgorithm(self, parameters, context, feedback):
        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT1', context)).source()
        tba_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT2', context)).source()
        output_path = self.parameterAsFileOutput(parameters, 'OUTPUT', context)
        algorithm = self.name()
        subprocess.run([PY_XDEM, SUBPROCESS_SCRIPT, algorithm, ref_dem_path, tba_dem_path, output_path], check=True)
        return _add_to_project(output_path=output_path, algorithm=algorithm)

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Coregistration'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

class Icp(Coregistration):
    def name(self):
        return 'ICP'
    def createInstance(self):
        return Icp()

class Lzd(Coregistration):
    def name(self):
        return 'LZD'
    def createInstance(self):
        return Lzd()

class NuthKaab(Coregistration):
    def name(self):
        return 'NuthKaab'
    def createInstance(self):
        return NuthKaab()