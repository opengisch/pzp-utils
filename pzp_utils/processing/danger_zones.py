from qgis import processing
from qgis.core import (
    QgsField,
    QgsFields,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterFeatureSink,
    QgsApplication,
)
from qgis.PyQt.QtCore import QVariant


class DangerZones(QgsProcessingAlgorithm):

    INPUT = "INPUT"
    MATRIX_FIELD = "MATRIX_FIELD"
    PROCESS_SOURCE_FIELD = "PROCESS_SOURCE_FIELD"
    OUTPUT = "OUTPUT"

    def createInstance(self):
        return DangerZones()

    def name(self):
        return "danger_zones"

    def displayName(self):
        return "Zone di pericolo"

    def group(self):
        return "Algoritmi"

    def groupId(self):
        return "algorithms"

    def shortHelpString(self):
        return "Algoritmo per il calcolo delle zone di pericolo"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, "Input layer", [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.MATRIX_FIELD,
                description="Campo contenente il valore della matrice",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.Numeric,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                name=self.PROCESS_SOURCE_FIELD,
                description="Campo contenente la fonte del processo",
                parentLayerParameterName=self.INPUT,
                type=QgsProcessingParameterField.String,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(self.OUTPUT, "Zone di pericolo")
        )

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)

        if source is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )

        fields = QgsFields()
        fields.append(QgsField("Grado di pericolo", QVariant.Int))

        matrix_field = self.parameterAsFields(
            parameters,
            self.MATRIX_FIELD,
            context,
        )[0]

        process_source_field = self.parameterAsFields(
            parameters,
            self.PROCESS_SOURCE_FIELD,
            context,
        )[0]

        # # Send some information to the user
        # feedback.pushInfo(f"CRS is {source.sourceCrs().authid()}")

        # if sink is None:
        #    raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        # Compute the number of steps to display within the progress bar and
        # total = 100.0 / source.featureCount() if source.featureCount() else 0


        used_matrix_values = set()
        process_sources  = set()

        for feature in source.getFeatures():
            process_sources.add(feature[process_source_field])
            used_matrix_values.add(feature[matrix_field])

        used_matrix_values = sorted(used_matrix_values, reverse=True)

        # -10 in the matrix is logically bigger than 0
        # -10 means "pericolo residuo", 0 is "non in pericolo"
        # so we swap them
        if 0 in used_matrix_values and -10 in used_matrix_values:
            used_matrix_values[-1], used_matrix_values[-2] = used_matrix_values[-2], used_matrix_values[-1]

        feedback.pushInfo(f"Used matrix values {used_matrix_values}")
        feedback.pushInfo(f"Process sources {process_sources}")

        final_layer = None
        for process_source in process_sources:
            result = self.prepare_process_source(used_matrix_values, process_source, matrix_field, process_source_field, parameters, context, feedback)

            if final_layer:
                result = processing.run(
                    "native:mergevectorlayers",
                    {
                        "LAYERS": [result["OUTPUT"], final_layer],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )
            final_layer = result["OUTPUT"]

        return {self.OUTPUT: final_layer}


    def prepare_process_source(self, used_matrix_values, process_source, matrix_field, process_source_field, parameters, context, feedback):
        final_layer = None
        for matrix_value in used_matrix_values:
            feedback.pushInfo(f'"{matrix_field}" = {matrix_value} AND "{process_source_field}" = \'{process_source}\'')
            result = processing.run(
                "native:extractbyexpression",
                {
                    "INPUT": parameters[self.INPUT],
                    "EXPRESSION": f'"{matrix_field}" = {matrix_value} AND "{process_source_field}" = \'{process_source}\'',
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )
            result = processing.run(
                "native:dissolve",
                {
                    "INPUT": result["OUTPUT"],
                    "FIELD": f"{matrix_field}",
                    "SEPARATE_DISJOINT": True,
                    "OUTPUT": "memory:",
                },
                context=context,
                feedback=feedback,
                is_child_algorithm=True,
            )

            if final_layer:
                result = processing.run(
                    "native:difference",
                    {
                        "INPUT": result["OUTPUT"],
                        "OVERLAY": final_layer,
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

                result = processing.run(
                    "native:mergevectorlayers",
                    {
                        "LAYERS": [result["OUTPUT"], final_layer],
                        "OUTPUT": "memory:",
                    },
                    context=context,
                    feedback=feedback,
                    is_child_algorithm=True,
                )

            final_layer = result["OUTPUT"]

        # Apply very small negative buffer to remove artifacts
        result = processing.run(
            "native:buffer",
            {
                "INPUT": final_layer,
                "DISTANCE": -0.0000001,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        # Snap to layer
        result = processing.run(
            "native:snapgeometries",
            {
                "INPUT": result["OUTPUT"],
                "REFERENCE_LAYER": result["OUTPUT"],
                "TOLERANCE": 0.1,
                "BEHAVIOR": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )
        # Snap to grid
        result = processing.run(
            "native:snappointstogrid",
            {
                "INPUT": result["OUTPUT"],
                "HSPACING": 0.001,
                "MSPACING": 0,
                "VSPACING": 0.001,
                "ZSPACING": 0,
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        result = processing.run(
            "native:multiparttosingleparts",
            {
                'INPUT': result["OUTPUT"],
                "OUTPUT": "memory:",
            },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        # qgis:deletecolumn has been renamed native:deletecolumn after qgis 3.16
        deletecolumn_id = "qgis:deletecolumn"
        if "qgis:deletecolumn" not in [x.id() for x in QgsApplication.processingRegistry().algorithms()]:
            deletecolumn_id = "native:deletecolumn"

        result = processing.run(
            deletecolumn_id,
            {'INPUT': result["OUTPUT"],
             'COLUMN':['fid', 'layer', 'path'],
             "OUTPUT": parameters[self.OUTPUT],
             },
            context=context,
            feedback=feedback,
            is_child_algorithm=True,
        )

        return result
