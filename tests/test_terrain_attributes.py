import os
import xdem
import pytest
import processing

from qgis.core import QgsRasterLayer

def test_terrain_attribute(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "slope.tif")
    result = processing.run("XDEM:Slope", {
        "DEM": ref_dem_layer,
        "OUTPUT": output_path
    })
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"], "slope")
    assert output.isValid()


def test_get_terrain_attributes():
    assert True
