import logging
from datetime import datetime
from typing import Type

from .exceptions import InvalidCameraException, InvalidQueryException
from .response import MarsRoverPhotosResponse, NasaResponse
from .restclient import RestClient
from .utils import get_api_key

CAMERAS = (
    "FHAZ",
    "RHAZ",
    "MAST",
    "CHEMCAM",
    "MAHLI",
    "MARDI",
    "NAVCAM",
    "PANCAM",
    "MINITES",
    "ALL",
)

EarthDate = datetime | str


class NasaClient(RestClient):
    limit_remaining: int

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.base_url = "https://api.nasa.gov"
        self.limit_remaining = None

        if (api_key := get_api_key(self.api_key) or "DEMO_KEY") is not None:
            self.update_params({"api_key": api_key})

    def mars_rover_photos(
        self,
        earth_date: EarthDate = None,
        sol: int = None,
        rover: str = "curiosity",
        camera: str = "ALL",
        page: int = 1,
        photo_limit: int = None,
    ) -> (Type[NasaResponse], bool):
        # validation checks
        if camera not in CAMERAS:
            raise InvalidCameraException(camera, CAMERAS)
        if sol is not None and earth_date is not None:
            raise InvalidQueryException(
                "Either 'sol' or 'earth_date' must be specified, not both."
            )
        if not isinstance(earth_date, (str, datetime)):
            raise TypeError(
                "'earth_date' must be a string in YYYY-MM-DD format or datetime object"
            )

        endpoint_url = f"mars-photos/api/v1/rovers/{rover}/photos"

        # add additional parameters to the request
        self.update_params({"page": page})

        if camera != "ALL":
            self.update_params({"camera": camera})

        if sol is not None:
            self.update_params({"sol": sol})
        elif earth_date is not None:
            self.update_params({"earth_date": parse_earth_date(earth_date)})

        # create target key for caching
        target_key = hash((rover, sol, earth_date, camera))

        # return from cache if exists
        if target_key in self.cache_strategy.cache:
            self.logger.info("Returning from cache")
            return self.cache_strategy.cache[target_key], True

        # process response
        response = self.get(endpoint_url)
        processed_response = MarsRoverPhotosResponse(
            response=response, limit=photo_limit
        )

        # save to cache
        self.cache_strategy.save(target_key, processed_response)

        # adjust limit_remaining
        self.limit_remaining = int(response.headers["X-RateLimit-Remaining"])
        return processed_response, False

    def curiosity_photos(
        self,
        earth_date: EarthDate = None,
        sol: int = None,
        camera: str = "ALL",
        page: int = 1,
        **kwargs,
    ) -> (Type[NasaResponse], bool):
        return self.mars_rover_photos(
            earth_date=earth_date,
            sol=sol,
            rover="curiosity",
            camera=camera,
            page=page,
            **kwargs,
        )

    def opportunity_photos(
        self,
        earth_date: EarthDate = None,
        sol: int = None,
        camera: str = "ALL",
        page: int = 1,
        **kwargs,
    ) -> (Type[NasaResponse], bool):
        return self.mars_rover_photos(
            earth_date=earth_date,
            sol=sol,
            rover="opportunity",
            camera=camera,
            page=page,
            **kwargs,
        )

    def spirit_photos(
        self,
        earth_date: EarthDate = None,
        sol: int = None,
        camera: str = "ALL",
        page: int = 1,
        **kwargs,
    ) -> (Type[NasaResponse], bool):
        return self.mars_rover_photos(
            earth_date=earth_date,
            sol=sol,
            rover="spirit",
            camera=camera,
            page=page,
            **kwargs,
        )


def parse_earth_date(earth_date: EarthDate) -> str:
    if isinstance(earth_date, datetime):
        return earth_date.strftime("%Y-%m-%d")
    return earth_date
