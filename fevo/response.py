from dataclasses import InitVar, dataclass, field
from typing import Any

import requests

from .models import Photo


@dataclass
class NasaResponse:
    response: InitVar[requests.Response]
    limit: int | None = None
    data: list = field(default_factory=list)

    def __post_init__(self, response: requests.Response) -> None:
        self.data = self.process_response(response)

    def process_response(self, response: requests.Response) -> list[Any]:
        raise NotImplementedError

    def _limit_processor(self, response: requests.Response) -> list[Any]:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self.data)


@dataclass
class MarsRoverPhotosResponse(NasaResponse):
    def process_response(self, response: requests.Response) -> list[Any]:
        photos = response.json()["photos"]

        if self.limit is not None:
            return self._limit_processor(photos)

        return [Photo.from_dict(photo_dict).img_src for photo_dict in photos]

    def _limit_processor(self, photos: list[dict]) -> list[Any]:
        processed = []

        for photo_dict in photos:
            if len(processed) < self.limit:
                processed.append(Photo.from_dict(photo_dict).img_src)
            else:
                return processed
