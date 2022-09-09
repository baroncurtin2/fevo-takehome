from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .utils import parse_date_strings


@dataclass
class Photo:
    id: int
    sol: int
    camera: Camera
    img_src: str
    earth_date: datetime
    rover: Rover

    @classmethod
    def from_dict(cls, photo_dict: dict) -> Photo:
        """Class method for instantiating Photo object from dictionary"""

        return cls(
            id=photo_dict.get("id"),
            sol=photo_dict.get("sol"),
            camera=Camera.from_dict(photo_dict.get("camera")),
            img_src=photo_dict.get("img_src"),
            earth_date=parse_date_strings(photo_dict.get("earth_date")),
            rover=Rover.from_dict(photo_dict.get("rover")),
        )


@dataclass
class Camera:
    id: int
    name: str
    rover_id: int
    full_name: str

    @classmethod
    def from_dict(cls, camera_dict: dict) -> Camera:
        """Class method for instantiating Camera object from dictionary"""

        return cls(
            id=camera_dict.get("id"),
            name=camera_dict.get("name"),
            rover_id=camera_dict.get("rover_id"),
            full_name=camera_dict.get("full_name"),
        )


@dataclass
class Rover:
    id: int
    name: str
    landing_date: datetime
    launch_date: datetime
    status: str

    @classmethod
    def from_dict(cls, rover_dict: dict) -> Rover:
        """Class method for instantiating Rover object from dictionary"""

        return cls(
            id=rover_dict.get("id"),
            name=rover_dict.get("name"),
            landing_date=parse_date_strings(rover_dict.get("landing_date")),
            launch_date=parse_date_strings(rover_dict.get("launch_date")),
            status=rover_dict.get("status"),
        )
