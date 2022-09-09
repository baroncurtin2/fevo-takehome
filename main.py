from fevo import NasaClient


def main(
    api_key: str = None,
    rover: str = "curiosity",
    camera: str = "ALL",
    start_date: str = None,
    end_date: str = None,
    img_limit: int = 3,
):
    client = NasaClient(api_key=api_key)


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
