import connexion
import six

from swagger_server.models.temperatue import Temperatue  # noqa: E501
from swagger_server import util


def get_temperatures():  # noqa: E501
    """get_temperatures

     # noqa: E501


    :rtype: List[Temperatue]
    """
    return 'do some magic!'


def set_temperature(body=None):  # noqa: E501
    """set_temperature

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Temperatue.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
