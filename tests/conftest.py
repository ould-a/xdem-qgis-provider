import os
import pytest
from qgis.core import QgsRasterLayer


@pytest.fixture
def ref_dem_layer():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    dem_path = os.path.join(test_dir, "../examples/longyearbyen_ref_dem.tif")
    layer = QgsRasterLayer(dem_path)
    assert layer.isValid()
    return layer


@pytest.fixture
def tba_dem_layer():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    dem_path = os.path.join(test_dir, "../examples/longyearbyen_tba_dem.tif")
    layer = QgsRasterLayer(dem_path)
    assert layer.isValid()
    return layer


@pytest.fixture
def stable_mask_layer():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    mask_path = os.path.join(test_dir, "../examples/inlier_mask.tif")
    mask_layer = QgsRasterLayer(mask_path)
    assert mask_layer.isValid()
    return mask_layer
