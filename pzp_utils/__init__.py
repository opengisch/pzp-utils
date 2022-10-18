from .pzp_utils import PZPUtilsPlugin


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load plugin.
    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    return PZPUtilsPlugin(iface)
