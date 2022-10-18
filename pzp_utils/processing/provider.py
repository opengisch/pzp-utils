from qgis.core import QgsProcessingProvider

from pzp_utils.processing.apply_matrix import ApplyMatrix
from pzp_utils.processing.danger_zones import DangerZones


class Provider(QgsProcessingProvider):
    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(DangerZones())
        self.addAlgorithm(ApplyMatrix())

    def id(self, *args, **kwargs):
        return "pzp"

    def name(self, *args, **kwargs):
        return self.tr("PZP")

    def icon(self):
        return QgsProcessingProvider.icon(self)
