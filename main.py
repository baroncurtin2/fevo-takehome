import requests
import json


def main():
    r = requests.get(
        "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date=2015-6-3&api_key=DEMO_KEY"
    )
    print(r.status_code)
    print(type(r.json()))
    print(json.dumps(r.json(), indent=4))


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
