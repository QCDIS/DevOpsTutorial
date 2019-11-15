import connexion
import six

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util


def add_student(body):  # noqa: E501
    """Add a new student

     # noqa: E501

    :param body: Student object that needs to be added
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_student(student_id):  # noqa: E501
    """delete_student

     # noqa: E501

    :param student_id: ID of pet to return
    :type student_id: int

    :rtype: Student
    """
    return 'do some magic!'
