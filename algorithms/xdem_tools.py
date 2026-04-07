import io
from contextlib import redirect_stdout


# Generic functions

def dem_info(dem, feedback, stats : bool = False) -> None:
    metadata = io.StringIO()
    with redirect_stdout(metadata):
        dem.info(stats=stats)
    feedback.pushInfo(metadata.getvalue())


def coreg_info(coreg, feedback) -> None:
    metadata = io.StringIO()
    with redirect_stdout(metadata):
        coreg.info()
    feedback.pushInfo(metadata.getvalue())
