import logging

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import traceback

logger = logging.getLogger(__name__)


class BDExceptionError(Exception):
    def __init__(self, *args: object, **kwargs: dict) -> None:
        self.code = kwargs['code']
        self.message = kwargs['message']


class ExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception) -> JsonResponse:
        traceback.print_exc()
        if isinstance(exception, ValueError):
            new_exception = BDExceptionError(code=40001, message='Invalid Parameter(s)')
        elif isinstance(exception, (
                BufferError,
                ArithmeticError,
                AssertionError,
                AttributeError,
                EnvironmentError,
                EOFError,
                ImportError,
                LookupError,
                MemoryError,
                NameError,
                ReferenceError,
                RuntimeError,
                SyntaxError)):
            new_exception = BDExceptionError(code=40002, message='Web Error')
        else:
            new_exception = BDExceptionError(code=500, message='NO FOUND ERROR')
        return JsonResponse(data={
            'message': new_exception.message,
            'code': new_exception.code,
            'detail': str(exception)
        }, status=400)
