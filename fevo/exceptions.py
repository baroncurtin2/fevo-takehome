from typing import Iterable


class MissingAPIKeyException(Exception):
    def __init__(self):
        msg = "Missing API key. Please provide API key via passed argument or environment variable."
        super().__init__(msg)


class InvalidCameraException(Exception):
    def __init__(self, invalid_camera: str, valid_cameras: Iterable[str]):
        msg = f"Invalid camera: {invalid_camera}. Camera must be one of {','.join(valid_cameras)}"
        super().__init__(msg)


class InvalidQueryException(Exception):
    """Invalid query wrapper exception"""

    pass
