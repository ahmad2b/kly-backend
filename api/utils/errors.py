class Missing(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Duplicate(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Invalid(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NotFound(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class BadRequest(HTTPError):
    def __init__(self, message):
        super().__init__(400, message)


class Unauthorized(HTTPError):
    def __init__(self, message):
        super().__init__(401, message)


class Forbidden(HTTPError):
    def __init__(self, message):
        super().__init__(403, message)


class UnprocessableEntity(HTTPError):
    def __init__(self, message):
        super().__init__(422, message)


class OK(HTTPError):
    def __init__(self, message):
        super().__init__(200, message)
