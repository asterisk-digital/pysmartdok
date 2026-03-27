import os

import dotenv

import pysmartdok


def main():
    dotenv.load_dotenv()
    client = pysmartdok.ApiClient(api_token=os.getenv("SMARTDOK_API_KEY"))

    data = client.rue.get_rue_summaries()
    print(data)


if __name__ == "__main__":
    main()
