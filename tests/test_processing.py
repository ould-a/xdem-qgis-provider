import os
import processing
from qgis.core import QgsRasterLayer


def test_slope(ref_dem_layer, tmp_path):
    output_path = os.path.join(tmp_path, "slope.tif")
    result = processing.run(
        "XDEM:Slope",
        {
            "DEM": ref_dem_layer,
            "SURFACE_FIT": "Florinsky",
            "UNIT": "Degrees",
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_coregistration(tba_dem_layer, ref_dem_layer, tmp_path):
    output_path = os.path.join(tmp_path, "aligned_dem.tif")
    result = processing.run(
        "XDEM:Coregistration",
        {
            "TBA_DEM": tba_dem_layer,
            "REF_DEM": ref_dem_layer,
            "MASK": None,
            "METHOD": "Nuth and Kääb (2011)",
            "BLOCKWISE": None,
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()
