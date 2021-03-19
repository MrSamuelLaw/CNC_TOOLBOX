
import functools
import traceback, sys
from PySide6.QtCore import QObject
from .models import Response


def PydanticSlot(model=None):
    """The PydanticSlot acts as a bridge between PySide slots
    that take and return json strings, and functions that take
    pydantic models as arguments."""
    def decorator(func):                                   # this is our actual decorator
        @functools.wraps(func)                             # this is allows us to debug easier
        def wrapper(*args, **kwargs):                      # this is where we wrap the function
            # check if in_model is provided
            if model is not None:
                try:
                    # check if method belongs to a class
                    if isinstance(args[0], QObject):
                        self, *payload = args             # seperate self & args
                        item = model.parse_raw(*payload)  # parse the payload
                        args = (self, item)               # create the arguments
                    else:
                        args = model.parse_raw(*args)     # if not class method, overwrite ags

                except Exception as e:
                    error_message = "\n".join([
                        f"failed on call to {func.__code__.co_name}",
                        f"from module {func.__module__}",
                        "with the following arguments:",
                        "\t\n".join([str(a) for a in args]),
                        "with the following error:",
                        str(e)
                    ])
                    return Response(status=False,
                                    message=error_message).json()

                else:
                    return func(*args, **kwargs).json()  # call the function if parsing successfull
        return wrapper                                   # return the wrapper
    return decorator                                     # return the decorator