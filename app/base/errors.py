class ApplicationError(Exception):
    def __init__(self, message: str):
        self.message = message

        super().__init__(self.message)


class ValidationError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
