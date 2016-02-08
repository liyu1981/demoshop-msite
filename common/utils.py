import logging
import inspect
import sys
from facebookads.exceptions import FacebookRequestError
from urllib import urlencode
from urlparse import urlparse, urlunparse
from django.shortcuts import render

logger = logging.getLogger(__name__)


def log_and_return_error(request, message=None):
    caller_module_name = __name__
    # get caller module name
    stack = inspect.stack()
    if len(stack) > 1:
        parentframe = stack[1][0]
        caller_module = inspect.getmodule(parentframe)
        caller_module_name = caller_module.__name__
    # get logger for caller module
    mlogger = logging.getLogger(caller_module_name)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    request.exception = exc_value
    if message is None:
        if exc_type == FacebookRequestError:
            message = exc_value.api_error_message()
        else:
            message = 'Oops. Something went wrong.'

    mlogger.error("Exception:", exc_info=(exc_type, exc_value, exc_traceback))

    return message


def log_and_show_error(request, message=None):
    message = log_and_return_error(request, message)
    return render(request, 'common/error.html', {'message': message})


def construct_url(url, params):
    parts = list(urlparse(url))
    parts[4] = urlencode(params)
    return urlunparse(parts)
