import xdem
from qgis.PyQt.QtCore import QCoreApplication

import io
from contextlib import redirect_stdout

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


# Generic functions
def dem_info(dem, feedback, stats: bool = False) -> None:

    metadata = io.StringIO()

    with redirect_stdout(metadata):
        dem.info(stats=stats)

    feedback.pushInfo(metadata.getvalue())


def coreg_info(coreg, feedback) -> None:

    metadata = io.StringIO()

    with redirect_stdout(metadata):
        coreg.info()

    feedback.pushInfo(metadata.getvalue())


class DemDifferencing(QgsProcessingAlgorithm):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT1', description='DEM 1'))
        self.addParameter(QgsProcessingParameterRasterLayer(name='INPUT2', description='DEM 2'))

        self.addParameter(QgsProcessingParameterRasterDestination(name='OUTPUT', description='DEM 1 - DEM 2'))
    
    def processAlgorithm(self, parameters, context, feedback):
        dem1_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT1', context=context)).source()
        dem2_path = (self.parameterAsRasterLayer(parameters=parameters, name='INPUT2', context=context)).source()
        output_path = self.parameterAsOutputLayer(parameters=parameters, name='OUTPUT', context=context)

        dem1 = xdem.DEM(dem1_path)
        dem_info(dem=dem1, feedback=feedback)
        dem2 = xdem.DEM(dem2_path)
        dem_info(dem=dem2, feedback=feedback)

        dem_dif = dem1 -dem2
        dem_info(dem=dem_dif, feedback=feedback, stats=True)

        dem_dif.to_file(output_path)
            
        return {'OUTPUT' : output_path}

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def name(self):
        return 'DEM differencing'
    
    def createInstance(self):
        return DemDifferencing()
    