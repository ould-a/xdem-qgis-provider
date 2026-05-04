import os
import pytest
import processing
from qgis.core import QgsRasterLayer


@pytest.fixture
def ref_dem_layer():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    dem_path = os.path.join(test_dir, "../examples/longyearbyen_ref_dem.tif")
    layer = QgsRasterLayer(dem_path, "dem_test")
    assert layer.isValid()
    return layer


def test_terrain_attribute(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "slope.tif")
    result = processing.run("XDEM:Slope", {
        "DEM": ref_dem_layer,
        "OUTPUT": output_path
    })
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"], "slope")
    assert output.isValid()