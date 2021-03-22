import functools
from PySide6.QtCore import QObject, Slot
from .models import Response


def PydanticSlot(model=None):
    """The PydanticSlot acts as a serialization layer between pure Python
    functions that take Pydantic Models as arguments, and a QML front end.

    The advantages are:
    * More readable code, with arguments being Pydantic Models,
      the "cognitave overhead" is reduced greatly.
    * Clearly defined endpoints.
    * Runtime validation.
    * Allows developers to determine if the problem with a function
      call is the arguments passed in, or the function implementation
      its self.
    """

    def inner(func):                                # Grab the functions
        @Slot(str, name=func.__name__, result=str)  # PySide string interface wrapper
        @functools.wraps(func)                      # Keeps our stack trace intact
        def wrapper(*args, **kwargs):               # The serialization is performed in the wrapper
            # check if in_model is provided
            if model is not None:
                try:
                    # check if method belongs to a PySide class
                    if isinstance(args[0], QObject):
                        self, *payload = args             # seperate into self & args
                        item = model.parse_raw(*payload)  # de-serialize the payload
                        args = (self, item)               # regenerate the argument tuple
                    else:
                        args = model.parse_raw(*args)     # de-serialize the payload

                except Exception as e:
                    error_message = "\n".join([
                        f"failed on call to {func.__code__.co_name}",  # which function was called
                        f"from module {func.__module__}",              # which module it belongs to
                        "with the following arguments:",
                        "\t\n".join([str(a) for a in args]),           # which arguments were passed in
                        "with the following error:",
                        str(e)                                         # the resulting error
                    ])
                    return Response(status=False,                      # return json response
                                    message=error_message).json()

                else:
                    return func(*args, **kwargs).json()                # return the json response
        return wrapper                                     # return the wrapper
    return inner                                      # return the decorator
