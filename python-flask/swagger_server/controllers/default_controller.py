import connexion
import six

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.temperature import Temperature  # noqa: E501
from swagger_server import util


def create_temperature(body=None):  # noqa: E501
    """create_temperature

    Creates a new Temperature # noqa: E501

    :param body: The Temperature to create
    :type body: dict | bytes

    :rtype: Temperature
    """
    if connexion.request.is_json:
        body = Temperature.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_temperature(_date):  # noqa: E501
    """get_temperature

    Gets a Temperature # noqa: E501

    :param _date: date of Temperature
    :type _date: str

    :rtype: Temperature
    """
    _date = util.deserialize_date(_date)
    return 'do some magic!'
