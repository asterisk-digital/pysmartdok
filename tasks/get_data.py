import os

import dotenv

import pysmartdok


def main():
    dotenv.load_dotenv()
    client = pysmartdok.ApiClient(api_token=os.getenv("SMARTDOK_API_TOKEN"))

    #qds = client.get_qd()
    data = client.get_projects()
    print(data)


if __name__ == '__main__':
    main()
