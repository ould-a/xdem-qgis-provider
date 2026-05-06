import processing
from qgis.core import QgsRasterLayer


def test_slope(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "slope.tif")
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


def test_aspect(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "aspect.tif")
    result = processing.run(
        "XDEM:Aspect",
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


def test_hillshade(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "hillshade.tif")
    result = processing.run(
        "XDEM:Hillshade",
        {
            "DEM": ref_dem_layer,
            "SURFACE_FIT": "Florinsky",
            "ALTITUDE": 45,
            "AZIMUTH": 315,
            "ZFACTOR": 1,
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()


def test_profile_curvature(ref_dem_layer, tmp_path):
    output_path = str(tmp_path / "profile_curvature.tif")
    result = processing.run(
        "XDEM:Profile curvature",
        {
            "DEM": ref_dem_layer,
            "SURFACE_FIT": "Florinsky",
            "CURV_METHOD": "geometric",
            "OUTPUT": output_path,
        },
    )
    assert "OUTPUT" in result
    output = QgsRasterLayer(result["OUTPUT"])
    assert output.isValid()
