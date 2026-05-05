import processing
from qgis.core import QgsRasterLayer


def test_terrain_attribute(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "slope.tif")
    result = processing.run("XDEM:Slope", {"DEM": ref_dem_layer, "OUTPUT": output_path})
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_coregistration(ref_dem_layer, tba_dem_layer, tmp_path):
    output_path = str(tmp_path / "aligned_dem.tif")
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


def test_bias_correction(ref_dem_layer, tba_dem_layer, tmp_path):
    output_path = str(tmp_path / "aligned_dem.tif")
    result = processing.run(
        "XDEM:Bias correction",
        {
            "TBA_DEM": tba_dem_layer,
            "REF_DEM": ref_dem_layer,
            "MASK": None,
            "METHOD": "Deramping",
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()
