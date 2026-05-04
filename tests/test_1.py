import os
import pytest
import processing
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


def test_terrain_attribute(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "test_slope.tif")
    result = processing.run("XDEM:Slope", {
        "DEM": ref_dem_layer,
        "OUTPUT": output_path
    })
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_coregistration(ref_dem_layer, tba_dem_layer, tmp_path):
    output_path = str(tmp_path / "test_aligned_dem.tif")
    result = processing.run("XDEM:Coregistration", {
        "TBA_DEM": tba_dem_layer,
        "REF_DEM": ref_dem_layer,
        "MASK": None,
        "METHOD": "Nuth and Kääb (2011)",
        "BLOCKWISE": None,
        "OUTPUT": output_path
    })
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()
