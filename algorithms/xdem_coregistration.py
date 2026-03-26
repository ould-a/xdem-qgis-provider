import xdem

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterRasterDestination)


# Coregistration

class Coreg(QgsProcessingAlgorithm):
    """
    Generic coregistration class, with a reference DEM, a to be aligned DEM as input and an output file for the aligned DEM.
    """

    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT1', self.tr('Ref DEM')))
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT2', self.tr('Tba DEM')))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT', self.tr(f'Aligned DEM {self.name()}')))
    
    def run_coregistration(self, parameters, context, feedback, coreg):
        """
        Function to load a reference DEM and a DEM to be aligned, apply the specified co-registration method, and save the result.
        """

        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT1', context)).source()
        tba_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT2', context)).source()
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)

        ref_dem = xdem.DEM(ref_dem_path)
        tba_dem = xdem.DEM(tba_dem_path)

        coreg.fit(ref_dem, tba_dem)
        aligned_dem = coreg.apply(tba_dem)

        aligned_dem.to_file(output_path)
        return {'OUTPUT' : output_path}

    def displayName(self):
        return self.tr(self.name())

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return 'Coregistration'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

class Icp(Coreg):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_coregistration(parameters=parameters, context=context, feedback=feedback, coreg=xdem.coreg.ICP())

    def name(self):
        return 'Iterative closest point'
    
    def createInstance(self):
        return Icp()
    
class Lzd(Coreg):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_coregistration(parameters=parameters, context=context, feedback=feedback, coreg=xdem.coreg.LZD())

    def name(self):
        return 'Least Z-difference'
    
    def createInstance(self):
        return Lzd()
    
class NuthKaab(Coreg):
    def processAlgorithm(self, parameters, context, feedback):
        return self.run_coregistration(parameters=parameters, context=context, feedback=feedback, coreg=xdem.coreg.NuthKaab())

    def name(self):
        return 'Nuth and Kaab'
    
    def createInstance(self):
        return NuthKaab()

# Tests
class BlockwiseNk(Coreg):
    def initAlgorithm(self, config = None):
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT1', self.tr('Ref DEM')))
        self.addParameter(QgsProcessingParameterRasterLayer('INPUT2', self.tr('Tba DEM')))
        self.addParameter(QgsProcessingParameterNumber('BLOCKSIZEFIT', self.tr('Block size fit'), defaultValue=500))
        self.addParameter(QgsProcessingParameterNumber('BLOCKSIZEAPPLY', self.tr('Block size apply'), defaultValue=1000))
        self.addParameter(QgsProcessingParameterRasterDestination('OUTPUT', self.tr(f'Aligned DEM {self.name()}')))

    def processAlgorithm(self, parameters, context, feedback):
        ref_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT1', context)).source()
        tba_dem_path = (self.parameterAsRasterLayer(parameters, 'INPUT2', context)).source()
        block_size_fit = self.parameterAsInt(parameters, 'BLOCKSIZEFIT', context)
        block_size_apply = self.parameterAsInt(parameters, 'BLOCKSIZEAPPLY', context)
        output_path = self.parameterAsOutputLayer(parameters, 'OUTPUT', context)
        
        ref_dem = xdem.DEM(ref_dem_path)
        tba_dem = xdem.DEM(tba_dem_path)

        coreg = xdem.coreg.BlockwiseCoreg(xdem.coreg.NuthKaab(),
                                      block_size_fit=block_size_fit,
                                      block_size_apply=block_size_apply,
                                      parent_path="")

        coreg.fit(ref_dem, tba_dem)
        aligned_dem = coreg.apply()

        aligned_dem.to_file(output_path)
        return {'OUTPUT' : output_path}

    def name(self):
        return 'Nuth and Kaab (Blockwise)'
    
    def createInstance(self):
        return BlockwiseNk()
