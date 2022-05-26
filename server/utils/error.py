class AppError(Exception):
    """
    Base class for application errors.
    """

    def __init__(self, message, *args, **kwargs) -> None:
        super().__init__(message, *args)
        self.payload = {"success": False, "message": message, **kwargs}
