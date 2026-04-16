from xdem.workflows import Topo

from .xdem_tools import XdemProcessingAlgorithm

from qgis.core import (QgsProcessingParameterFile,
                       )


class TopoWorkflow(XdemProcessingAlgorithm):

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterFile(
            name='CONFIG',
            description='Config file'))
        
    def processAlgorithm(self, parameters, context, feedback):
        config_file = self.parameterAsString(parameters, 'CONFIG', context)
        workflows = Topo(config_file)
        workflows.run()
        return {}
    
    def name(self):
        return 'Topography'

    def shortHelpString(self):
        return "/" 

    def createInstance(self):
        return TopoWorkflow()
