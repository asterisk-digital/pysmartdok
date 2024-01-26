from multiprocessing import Pool
import datetime
import sys
import logging
import json

from bs4 import BeautifulSoup as bs
import requests

# TODO: REMOVE AFTER DEVELOPMENT
## FIXME: REMOVE ALL BELOW CODE UP TO NEXT FIXME
import os
from pathlib import Path
import dotenv

script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

envfile = Path(script_dir.parent, '.env')
if not envfile.exists():
    print(f'envfile {envfile} not found')
    exit(1)

dotenv.load_dotenv(dotenv_path=envfile)

envvars = {}

# envvars that are required to run
required_envvars = ['SMARTDOK_USERNAME', 'SMARTDOK_PASSWORD', 'SMARTDOK_INTEGRATION_TOKEN']
for required_envvar in required_envvars:
    if required_envvar not in os.environ:
        print('Error: Required envvar not in environment: ' + required_envvar)
        exit(1)

    envvars[required_envvar] = os.environ[required_envvar]

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug(f'envvars: {envvars}')
## FIXME: REMOVE ALL ABOVE CODE UP TO NEXT FIXME
# TODO: REMEMBER TO REMOVE AFTER DEVELOPMENT

class Client:
    def __init__(self, username: str = None, password: str = None, integration_token: str = None, user_agent: str = 'intrix-pysmartdok(post@intrix.no)'):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        
        if None in (username, password, integration_token):
            raise ValueError("username, password, and integration token must be provided.")

        self.session = requests.Session()
        # TODO: ADD CONMMENT ABOUT WHY WE USE THIS USER AGENT
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 [{user_agent}]',
            'X-CSRF': '',
        }
        self.session.headers.update(headers)
        logging.debug(f'current headers for session: \n {self.session.headers}')

        self.base_url = 'https://web.smartdok.no'
        self.web_api_url = f'{self.base_url}/smartapi'

        login = self.inisiat_smartdok_web_api(username, password)

    def inisiat_smartdok_web_api(self, username: str, password: str):
        if self.smartdok_web_login(username, password) == 200: logging.debug('smartdok_web_login - success')
        self.inisiat_api()

    def smartdok_web_login(self, username: str, password: str) -> requests.status_codes:
        # TODO: ADD CONMMENT ABOUT WHY WE HAVE STRUCTURED THE FORM DATA LIKE THIS
        raw_form_data = {
            'eventtarget':          {'key': '__EVENTTARGET', 'value': ''},
            'eventargument':        {'key': '__EVENTARGUMENT', 'value': ''},
            'viewstate':            {'key': '__VIEWSTATE', 'value': ''},
            'viewstategenerator':   {'key': '__VIEWSTATEGENERATOR', 'value': ''},
            'eventvalidation':      {'key': '__EVENTVALIDATION', 'value': ''},
            'forgerytoken':         {'key': 'SmartDokLoginView$LoginSmartDok$__antiForgeryToken', 'value': ''},
            'username':             {'key': 'SmartDokLoginView$LoginSmartDok$UserName', 'value': username},
            'password':             {'key': 'SmartDokLoginView$LoginSmartDok$Password', 'value': password},
            'loginbutton':          {'key': 'SmartDokLoginView$LoginSmartDok$LoginButton', 'value': ''}
        }
        logging.debug(f'smartdok_web_login - form_data: {raw_form_data}')

        login_page = self.session.get(self.base_url)
        soup = bs(login_page.text, 'html.parser')

        for meta_key, inner_dict in raw_form_data.items():
            # TODO: ADD CONMMENT ABOUT WHY WE SKIP USERNAME AND PASSWORD
            if meta_key == 'username' or meta_key == 'password':
                continue
            inner_dict['value'] = self.soup_find_input_value(soup, inner_dict['key'])

        form_data = self.dict_with_dict_to_dict(raw_form_data)

        response = self.session.post(f'{self.base_url}/index.aspx', data=form_data)

        if response.status_code != 200:
            raise Exception(f'Login failed {response.status_code}')
        
        response_soup = bs(response.text, 'html.parser')

        if response_soup.find('span', attrs={'id': 'LabelCompanyName'}).text == None:
            raise Exception('Login failed - no company name found')

        logging.debug(f'smartdok_web_login - response_soup: {response_soup}')

        return response.status_code
    

        
    def inisiat_api(self):
        payload = {
            'Submitter': '',
            'DepartmentId': '',
            'FromDate': '',
            'ToDate': '',
            'IncludeDeactivated': 'false',
            'HideStatus[]': '3',
            'take': '20',
            'skip': '0',
            'page': '1',
            'pageSize': '20'
        }


        test = self.session.get(f'{self.web_api_url}/qd/overview' , params=payload)

        # make text to dict
        test = json.loads(test.text)

        print(test)

    @staticmethod
    def soup_find_input_value(soup: bs, input_name: str) -> str:
        """
        soup_find_input is a static method that is used to find the value of an input element in a BeautifulSoup object.

        Parameters:
        - soup (BeautifulSoup): The BeautifulSoup object to search in.
        - input_name (str): The name attribute of the input element to find.

        Returns:
        - str: The value of the found input element.
        """
        input = soup.find('input', attrs={'name': input_name})

        if input == None:
            raise Exception(f'no input found with name {input_name}')

        input_value = input['value']
        
        logging.debug(f'soup_find_input - name={input_name}, value={input_value}')

        return input_value
    
    @staticmethod
    def dict_with_dict_to_dict(input_dict: dict) -> dict:
        """
        Converts a dictionary with nested dictionaries to a flat dictionary.

        Args:
            input_dict (dict): The input dictionary with nested dictionaries.

        Returns:
            dict: The resulting flat dictionary.
        """
        output_dict = {}

        for key in input_dict:
            return_key = input_dict[key]['key']
            output_dict[return_key]= input_dict[key]['value']
            
        logging.debug(f'dict_with_dict_to_dict - from {input_dict} \n to {output_dict}')
            
        return output_dict


if __name__ == "__main__":
    client = Client(envvars['SMARTDOK_USERNAME'], envvars['SMARTDOK_PASSWORD'], envvars['SMARTDOK_INTEGRATION_TOKEN'])