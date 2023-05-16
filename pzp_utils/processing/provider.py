from qgis.core import QgsProcessingProvider

from pzp_utils.processing.apply_matrix import ApplyMatrix
from pzp_utils.processing.danger_zones import DangerZones
from pzp_utils.processing.simplify_intensity import SimplifyIntensity
from pzp_utils.processing.merge_intensity_layers import MergeIntensityLayers
from pzp_utils.processing.fix_geometries import FixGeometries
from pzp_utils.processing.no_impact import NoImpact
from pzp_utils.processing.propagation import Propagation
from pzp_utils.processing.remove_overlappings import RemoveOverlappings


class Provider(QgsProcessingProvider):
    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(DangerZones())
        self.addAlgorithm(ApplyMatrix())
        self.addAlgorithm(SimplifyIntensity())
        self.addAlgorithm(MergeIntensityLayers())
        self.addAlgorithm(FixGeometries())
        self.addAlgorithm(NoImpact())
        self.addAlgorithm(Propagation())
        self.addAlgorithm(RemoveOverlappings())

    def id(self, *args, **kwargs):
        return "pzp"

    def name(self, *args, **kwargs):
        return self.tr("PZP")

    def icon(self):
        return QgsProcessingProvider.icon(self)
