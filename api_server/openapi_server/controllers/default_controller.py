import configparser
import datetime
import json
import os
from copy import copy
from pathlib import Path

import connexion
import pymongo


from openapi_server import util
from openapi_server.models.temperature import Temperature

properties_path = 'properties.ini'
if not os.path.isfile(properties_path):
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    properties_path = os.path.join(current_path.parent, 'properties.ini')


config = configparser.ConfigParser()
config.read(properties_path)

mongo_client = pymongo.MongoClient(config['mongo']['endpotin'])
db = mongo_client["tmp_service_database"]
collection = db["temperatures"]


def create_temperature(body=None):  # noqa: E501
    """create_temperature

    Creates a new Temperature # noqa: E501

    :param body: The Temperature to create
    :type body: dict | bytes

    :rtype: Temperature
    """
    if connexion.request.is_json:
        body = connexion.request.get_json()  # noqa: E501
        body['date'] = str(datetime.datetime.now())
        temp = copy(body)
        result = collection.insert_one(body)
        return temp
    return 'Wrong request',400


def get_temperature():  # noqa: E501
    """get_temperature

    Gets a Temperature # noqa: E501

    :param _date: date of Temperature
    :type _date: str

    :rtype: Temperature
    """
    cursor = collection.find({})
    max = -100
    max_temp = {}
    for temp in cursor:
        if temp['value'] > max:
            max = temp['value']
            max_temp['value'] = temp['value']
            max_temp['date'] = temp['date']

    return max_temp