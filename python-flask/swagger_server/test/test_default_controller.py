# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_message import ErrorMessage  # noqa: E501
from swagger_server.models.temperature import Temperature  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_temperature(self):
        """Test case for create_temperature

        
        """
        body = Temperature()
        response = self.client.open(
            '/my-temp-service/0.0.1/Temperatures',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_temperature(self):
        """Test case for get_temperature

        
        """
        query_string = [('_date', '2013-10-20')]
        response = self.client.open(
            '/my-temp-service/0.0.1/Temperatures',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
