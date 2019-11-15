# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.student import Student  # noqa: E501
from swagger_server.test import BaseTestCase


class TestPetController(BaseTestCase):
    """PetController integration test stubs"""

    def test_get_student_by_id(self):
        """Test case for get_student_by_id

        Find student by ID
        """
        query_string = [('subject', 'subject_example')]
        response = self.client.open(
            '/service-api/pet/{student_id}'.format(student_id=789),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
