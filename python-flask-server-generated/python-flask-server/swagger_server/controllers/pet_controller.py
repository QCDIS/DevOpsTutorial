import connexion
import six

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util


def get_student_by_id(student_id, subject=None):  # noqa: E501
    """Find student by ID

    Returns a single pet # noqa: E501

    :param student_id: ID of pet to return
    :type student_id: int
    :param subject: The subject name
    :type subject: str

    :rtype: Student
    """
    return 'do some magic!'
