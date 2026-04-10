import io

from contextlib import redirect_stdout
from qgis.utils import iface
from qgis.core import QgsProcessingAlgorithm
from qgis.PyQt.QtCore import QCoreApplication


# Generic functions
def dem_info(dem, feedback, stats : bool = False) -> None:
    metadata = io.StringIO()
    with redirect_stdout(metadata):
        dem.info(stats=stats)
    feedback.pushInfo(metadata.getvalue())


def coreg_info(coreg, feedback) -> None:
    metadata = io.StringIO()
    with redirect_stdout(metadata):
        coreg.info()
    feedback.pushInfo(metadata.getvalue())


# Generic processing class
class XdemProcessingAlgorithm(QgsProcessingAlgorithm):

    def flags(self):
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
    
    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)
