import configparser
import datetime
import json
from copy import copy

import connexion
import pymongo

from openapi_server import util
from openapi_server.models.temperature import Temperature

config = configparser.ConfigParser()
config.read('properties.ini')

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