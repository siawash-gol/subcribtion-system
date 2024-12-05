from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    handlers = {
        'ValidationError': _handler_generic_error,
        'Http404': _handler_generic_error,
        'PermissionDenied': _handler_generic_error,
        'NotAuthenticated': _handler_authenticated_error

    }
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handler_authenticated_error(exc, context, response):
    response.data = {
        'error': 'Please login to proceed',
        'status_code': response.status_code
    }


def _handler_generic_error(exc, context, response):
    return response
