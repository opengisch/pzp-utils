from collections import OrderedDict

from qgis import processing
from qgis.core import (
    QgsFeature,
    QgsFeatureSink,
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMatrix,
    QgsProcessingParameterEnum,
    edit,
)
from qgis.PyQt.QtCore import QVariant

from . import domains


class NoImpact(QgsProcessingAlgorithm):

    AREA_LAYER = "AREA_LAYER"
    INTENSITY_LAYER = "INTENSITY_LAYER"
    PERIOD_FIELD = "PERIOD_FIELD"
    INTENSITY_FIELD = "INTENSITY_FIELD"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return NoImpact()

    def name(self):
        return "no_impact"

    def displayName(self):
        return "Zone nessun impatto"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per calcolare le zone di nessun impatto"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.AREA_LAYER,
                "Layer con l'area di studio",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INTENSITY_LAYER,
                "Layer con l'intensità",
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PERIOD_FIELD,
                description="Campo contenente il periodo di ritorno",
                parentLayerParameterName=self.INTENSITY_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.INTENSITY_FIELD,
                description="Campo contenente l'intensità",
                parentLayerParameterName=self.INTENSITY_LAYER,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Nessun impatto")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INTENSITY_LAYER, context)
        intensity_layer = self.parameterAsVectorLayer(parameters, self.INTENSITY_LAYER, context)
        period_field = self.parameterAsFields(
            parameters,
            self.PERIOD_FIELD,
            context,
        )[0]

        intensity_field = self.parameterAsFields(
            parameters,
            self.INTENSITY_FIELD,
            context,
        )[0]

        used_periods = set()

        attributes = None

        period_field_idx = -1
        intensity_field_idx = -1

        one_feature = next(source.getFeatures())
        if one_feature:
            period_field_idx = one_feature.fieldNameIndex(period_field)
            intensity_field_idx = one_feature.fieldNameIndex(intensity_field)

        for feature in source.getFeatures():
            used_periods.add(feature[period_field])
            attributes = feature.attributes()

        used_periods = sorted(used_periods, reverse=False)

        feedback.pushInfo(f"Used periods {used_periods}")

        fields = source.fields()
        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            fields,
            source.wkbType(),
            source.sourceCrs(),
        )

        for period in used_periods:
            result = processing.run(
                "native:extractbyexpression",
                {
                    "INPUT": parameters[self.INTENSITY_LAYER],
                    "EXPRESSION": f'"{period_field}" = {period}',
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            result = processing.run(
                "native:difference",
                {
                    'INPUT': parameters[self.AREA_LAYER],
                    'OVERLAY': result["OUTPUT"],
                    'OUTPUT': "memory:",
                    'GRID_SIZE':None,
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            result = processing.run(
                "native:multiparttosingleparts",
                {
                    'INPUT': result["OUTPUT"],
                    'OUTPUT': "memory:",
                },
                context=context,
                feedback=feedback,
                # is_child_algorithm=True,
            )

            for feature in result["OUTPUT"].getFeatures():
                attributes[period_field_idx] = period
                attributes[intensity_field_idx] = 1000

                feature.setAttributes(attributes)

                # TODO rimuovere fid
                sink.addFeature(feature)

        return {self.OUTPUT: dest_id}
