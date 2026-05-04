import os
import xdem
import pytest
import processing

from qgis.core import QgsRasterLayer

def test_load_dem():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    origin_dem_path = os.path.join(base_dir, "longyearbyen_ref_dem.tif")
    
    layer = QgsRasterLayer(origin_dem_path, "dem")
    assert layer.isValid()

    qgis_dem_path = layer.dataProvider().dataSourceUri()
    assert origin_dem_path == qgis_dem_path