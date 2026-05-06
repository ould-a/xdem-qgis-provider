import processing
from qgis.core import QgsRasterLayer


def test_coregistration(tba_dem_layer, ref_dem_layer, tmp_path):
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


def test_coregistration_with_mask(tba_dem_layer, ref_dem_layer, stable_mask_layer, tmp_path):
    output_path = str(tmp_path / "aligned_dem.tif")
    result = processing.run(
        "XDEM:Coregistration",
        {
            "TBA_DEM": tba_dem_layer,
            "REF_DEM": ref_dem_layer,
            "MASK": stable_mask_layer,
            "METHOD": "Nuth and Kääb (2011)",
            "BLOCKWISE": None,
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_blockwise_coregistration(tba_dem_layer, ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "aligned_dem.tif")
    result = processing.run(
        "XDEM:Coregistration",
        {
            "TBA_DEM": tba_dem_layer,
            "REF_DEM": ref_dem_layer,
            "MASK": None,
            "METHOD": "Nuth and Kääb (2011)",
            "BLOCKWISE": 1000,
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_bias_correction(tba_dem_layer, ref_dem_layer, tmp_path):
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


def test_bias_correction_with_mask(tba_dem_layer, ref_dem_layer, stable_mask_layer, tmp_path):
    output_path = str(tmp_path / "aligned_dem.tif")
    result = processing.run(
        "XDEM:Bias correction",
        {
            "TBA_DEM": tba_dem_layer,
            "REF_DEM": ref_dem_layer,
            "MASK": stable_mask_layer,
            "METHOD": "Deramping",
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()