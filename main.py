#!/usr/bin/env python3

import datetime

from fevo import NasaClient, parse_date_strings


def main(
    api_key: str = None,
    rover: str = "curiosity",
    camera: str = "ALL",
    start_date: str = None,
    end_date: str = None,
    img_limit: int = 3,
) -> dict[str, list[str]]:
    client = NasaClient(api_key=api_key)
    return get_day_range_photo_links(
        client, rover, camera, start_date, end_date, img_limit
    )


def get_days_photo_links(
    client: NasaClient,
    rover: str,
    camera: str,
    earth_date: str | datetime.datetime,
    img_limit: int,
) -> list[str]:
    response, _ = client.mars_rover_photos(
        earth_date=earth_date, rover=rover, camera=camera, photo_limit=img_limit
    )
    return response.data


def get_day_range_photo_links(
    client: NasaClient,
    rover: str,
    camera: str,
    start_date: str,
    end_date: str = None,
    img_limit: int = None,
    timedelta: int = 10,
) -> dict[str, list[str]]:
    start_date, end_date = parse_date_strings(start_date), parse_date_strings(end_date)

    if end_date is None:
        date_range = [start_date + datetime.timedelta(days=i) for i in range(timedelta)]

    else:
        date_range = [
            start_date + datetime.timedelta(days=i)
            for i in range((end_date - start_date).days)
        ]

    return {
        earth_date.strftime("%Y-%m-%d"): get_days_photo_links(
            client, rover, camera, earth_date, img_limit
        )
        for earth_date in date_range
    }


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    photos = main(
        api_key="qZ5V1pMbsXhQbaa8y5ixnOhAbTpHN695Jd4yfnTU",
        start_date="2022-01-01",
        img_limit=3,
    )
    print(photos)
