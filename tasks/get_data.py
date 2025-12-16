import os
import sys
from pathlib import Path

import dotenv

script_dir = os.path.dirname(os.path.realpath(__file__))

sys.path.append(script_dir + "../src")

from pysmartdok import apiclient


def main():
    envfile = script_dir + "/../.env-prod"
    if not Path(envfile).exists():
        raise FileNotFoundError(f"Could not find envfile: {envfile}")

    dotenv.load_dotenv(envfile)
    client = apiclient.ApiClient(api_token=os.getenv("SMARTDOK_API_TOKEN"))

    qds = client.get_qd()
    print(qds)


if __name__ == '__main__':
    main()
