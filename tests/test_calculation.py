from qgis.core import QgsFeature, QgsProject, QgsRelation, QgsVectorLayer
from qgis.gui import QgsAttributeEditorContext
from qgis.PyQt.QtCore import Qt
from qgis.testing import start_app, unittest

from pzp_utils.processing.merge_by_area import MergeByArea

start_app()


class TestMergeByForm(unittest.TestCase):

    def test_MergeByForm(self):
        
        self.assertTrue(False)

