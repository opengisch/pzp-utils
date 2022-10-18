import os
from qgis.PyQt.QtCore import (
    QTranslator,
    QCoreApplication)
from qgis.core import QgsApplication
from qgis.gui import QgisInterface
from pzp_utils.processing.provider import Provider

class PZPUtilsPlugin:
    """QGIS Plugin Implementation."""

    def __init__(self, iface: QgisInterface):
        super().__init__()
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        self.provider = Provider()

    def initProcessing(self):
        """Create the Processing provider"""
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Creates application GUI widgets"""
        self.initProcessing()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        QgsApplication.processingRegistry().removeProvider(self.provider)
