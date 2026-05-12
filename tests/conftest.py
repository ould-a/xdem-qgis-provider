import os
import xdem
import pytest
import geoutils as gu
from qgis.core import QgsRasterLayer


@pytest.fixture
def ref_dem_layer():
    ref_dem_path = xdem.examples.get_path("longyearbyen_ref_dem")
    layer = QgsRasterLayer(ref_dem_path)
    return layer


@pytest.fixture
def tba_dem_layer():
    tba_dem_path = xdem.examples.get_path("longyearbyen_tba_dem")
    layer = QgsRasterLayer(tba_dem_path)
    return layer


@pytest.fixture
def stable_mask_layer(tmp_path):
    ref_dem = xdem.DEM(xdem.examples.get_path("longyearbyen_ref_dem"))
    glacier_outlines = gu.Vector(
        xdem.examples.get_path("longyearbyen_glacier_outlines")
    )
    stable_mask = ~glacier_outlines.create_mask(ref_dem)
    stable_mask_path = os.path.join(tmp_path, "stable_mask.tif")
    stable_mask.to_file(stable_mask_path)
    layer = QgsRasterLayer(stable_mask_path)
    return layer
