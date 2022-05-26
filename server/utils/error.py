class AppError(Exception):
    """
    Base class for application errors.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args)
        self.status_code = kwargs.get('status_code', 500)
        self.message = kwargs.get('message', 'Internal Server Error')