import xdem
from qgis.PyQt.QtCore import QCoreApplication

import io
from contextlib import redirect_stdout


# Generic functions

def xdem_object_info(xdem_object, feedback, stats: bool = False) -> None:
    metadata = io.StringIO()

    with redirect_stdout(metadata):
        xdem_object.info(stats=stats)

    feedback.pushInfo(metadata.getvalue())
