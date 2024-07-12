# This work is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License.
# https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode

from typing import Any

from django.http import HttpResponse
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


def status_code_handler(exc: APIException, context: Any) -> HttpResponse:
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 403:
        response.status_code = 401

    return response
