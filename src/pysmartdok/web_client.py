import logging
from multiprocessing import Pool, cpu_count

import requests
from bs4 import BeautifulSoup

from . import pysmartdok_utils


class WebClient:
    def __init__(
        self,
        username: str = None,
        password: str = None,
        user_agent: str = "intrix-pysmartdok(post@intrix.no)",
    ):
        """
        initializes an instance of the `pysmartdok` class.

        args:
            username (str, required): the username for SmartDok login. defaults to None.
            password (str, required): the password for SmartDok login. defaults to None.
            user_agent (str, optional): the user agent to be used for the HTTP requests. defaults to 'intrix-pysmartdok(post@intrix.no)'.
        """
        logging.basicConfig(
            level=logging.DEBUG, format="[%(levelname)s] - %(asctime)s - %(message)s"
        )
        pysmartdok_utils.verify_init_params(username, password, user_agent)

        # we use this user agent because SmartDok blocks the default Python user agent.
        # it's necessary to employ a user agent that SmartDok does not block.
        # the 'X-CSRF' header is required by SmartDok to prevent CSRF attacks.
        # we initialize it to be empty as its specific value is unknown; it only needs to be present in the headers.
        headers = {
            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 [{user_agent}]",
            "X-CSRF": "",
        }

        self.session = requests.Session()
        self.session.headers.update(headers)

        self.base_url = "https://web.smartdok.no"
        self.web_api_url = f"{self.base_url}/smartapi"

        response = self.smartdok_login(username, password)
        if response.status_code != 200:
            raise Exception(f"request status code {response.status_code} != 200")

    def smartdok_login(
        self, username: str = None, password: str = None
    ) -> requests.Response:
        """
        logs into the SmartDok website using the provided username and password.

        args:
            username (str): the username for logging into SmartDok.
            password (str): the password for logging into SmartDok.

        returns:
            int: the status code of the login request.

        raises:
            Exception: if the login request fails or the login is unsuccessful.
        """
        # we have structured the form data like this because we need to retrieve the values of the hidden inputs.
        # this approach helps avoid the need to write the long key name every time we interact with the hidden input values.
        raw_form_data = {
            "viewstate": {"key": "__VIEWSTATE", "value": ""},
            "viewstategenerator": {"key": "__VIEWSTATEGENERATOR", "value": ""},
            "eventvalidation": {"key": "__EVENTVALIDATION", "value": ""},
            "forgerytoken": {
                "key": "SmartDokLoginView$LoginSmartDok$__antiForgeryToken",
                "value": "",
            },
            "username": {
                "key": "SmartDokLoginView$LoginSmartDok$UserName",
                "value": username,
            },
            "password": {
                "key": "SmartDokLoginView$LoginSmartDok$Password",
                "value": password,
            },
            "loginbutton": {
                "key": "SmartDokLoginView$LoginSmartDok$LoginButton",
                "value": "",
            },
        }

        login_page = self.session.get(self.base_url)
        soup = BeautifulSoup(login_page.text, "html.parser")

        for meta_key, inner_dict in raw_form_data.items():
            # we skip username and password because we already have them in the raw_form_data dict.
            if meta_key == "username" or meta_key == "password":
                continue
            inner_dict["value"] = pysmartdok_utils.soup_find_input_value(
                soup, inner_dict["key"]
            )

        form_data = pysmartdok_utils.dict_with_dict_to_dict(raw_form_data)

        login = self.session.post(f"{self.base_url}/index.aspx", data=form_data)

        pysmartdok_utils.verify_login(login)

        return login

    def get_single_record(self, record_id: str = None, record_type: str = None) -> dict:
        """
        retrieves a single record from the SmartDok API.

        args:
            record_id (str): the ID of the record to retrieve.
            record_type (str): the type of the record to retrieve.

        returns:
            dict: the processed data of the retrieved record.

        raises:
            Exception: if the request to the API fails.
            ValueError: if the record_type is unknown.
        """
        pysmartdok_utils.verify_record_type(record_type)

        params = {"id": record_id, "getAccessRights": "true"}

        response = self.session.get(
            f"{self.web_api_url}/{record_type}/report", params=params
        )

        if response.status_code != 200:
            raise Exception(f"request status code {response.status_code} != 200")

        respone_data = response.json()

        if record_type == "qd":
            processed_data = pysmartdok_utils.convert_smartdok_qd_record_to_dict(
                respone_data
            )
        elif record_type == "rue":
            processed_data = pysmartdok_utils.convert_smartdok_rue_record_to_dict(
                respone_data
            )
        else:
            raise ValueError(f"Unknown record_type: {record_type}")

        return processed_data

    def get_single_record_wrapper(self, args):
        """
        wrapper method for getting a single record.

        args:
            args: the arguments to be passed to the `get_single_record` method.

        returns:
            the result of the `get_single_record` method.
        """
        return self.get_single_record(*args)

    def get_all_records(self, record_type: str = None, days_back: int = 0) -> list:
        """
        retrieves all records of a specified type within a given time range.

        args:
            record_type (str): the type of records to retrieve.
            days_back (int): the number of days back from the current date to retrieve records.

        returns:
            list: a list of records.

        raises:
            ValueError: if the record_type is invalid.

        """
        pysmartdok_utils.verify_record_type(record_type)

        records = []

        if days_back > 0:
            today_date, days_back_date = (
                pysmartdok_utils.convert_date_to_smartdok_date_format(days_back)
            )
        else:
            today_date = ""
            days_back_date = ""

        params = {
            "FromDate": days_back_date,
            "ToDate": today_date,
            "take": "",
        }

        response_all_records = self.session.get(
            f"{self.web_api_url}/{record_type}/overview", params=params
        )

        # remove .text = the JSON object must be str, bytes or bytearray, not Response
        response_all_records_data_raw = response_all_records.json()
        response_all_records_data = response_all_records_data_raw["data"]

        record_ids = [record["Id"] for record in response_all_records_data]

        # set the number of processes you want to use (adjust as needed)
        num_processes = cpu_count()

        # create a pool of processes
        with Pool(processes=num_processes) as p:
            # use pool.map to parallelize the execution of get_single_record
            record_args = [(record_id, record_type) for record_id in record_ids]
            # this line is using the map method of the pool to apply the get_single_record_wrapper function to every item in record_args. The map method blocks until all the function calls are completed. The results are returned as a list and assigned to records.
            records = p.map(self.get_single_record_wrapper, record_args)
        p.close()
        p.join()

        return records
