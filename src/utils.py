import logging
from bs4 import BeautifulSoup as bs
import requests

import datetime
from datetime import timezone, timedelta

def soup_find_input_value(soup: bs, input_name: str) -> str:
    """
    soup_find_input_value is a static method that is used to find the value of an input element in a BeautifulSoup object.

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
    
    logging.debug(f'soup_find_input_value - name={input_name}, value={input_value}')

    return input_value

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


def verify_login(website: requests.Response = None) -> bool:
    if website.status_code != 200:
        raise Exception(f'request status code {website.status_code} != 200')
    
    soup = bs(website.text, 'html.parser')

    # span with id LabelCompanyName is only present when logged in successfully
    if soup.find('span', attrs={'id': 'LabelCompanyName'}) == None:
        raise Exception('no span with id LabelCompanyName found')


import os
from pathlib import Path
import dotenv

def load_dotenv():
    script_dir = Path(os.path.dirname(os.path.realpath(__file__)))

    envfile = Path(script_dir.parent, '.env')
    if not envfile.exists():
        print(f'envfile {envfile} not found')
        exit(1)

    dotenv.load_dotenv(dotenv_path=envfile)

    envvars = {}

    required_envvars = ['SMARTDOK_USERNAME', 'SMARTDOK_PASSWORD', 'SMARTDOK_INTEGRATION_TOKEN']
    for required_envvar in required_envvars:
        if required_envvar not in os.environ:
            print('Error: Required envvar not in environment: ' + required_envvar)
            exit(1)

        envvars[required_envvar] = os.environ[required_envvar]

    logging.debug(f'envvars: {envvars}')

    return envvars

def convert_smartdok_rue_record_to_dict(record: dict) -> dict:
    pass

def convert_smartdok_qd_record_to_dict(raw_record: dict) -> dict:
    record = {
        'recordtype': 'qd',
        'title': raw_record['Title'],
        'description': raw_record['Description'],
        'status': raw_record['Status'],
        'category': 'category', # need to get with special means    
        'id': raw_record['Id'],
        'deviationid': raw_record['DeviationId'],
        'submitdate': raw_record['SubmitDate'],
        'project': {
            'id': raw_record['ProjectId'],
            'name': raw_record['ProjectName'],
            'number': raw_record['ProjectNumber']
        },
        'subproject': {
            'id':  raw_record['SubProjectId'],
            'name': raw_record['SubProjectName'],
            'number': raw_record['SubProjectNumber']
        },
        'submitter': {
            'id': raw_record['SubmitterId'],
            'name': raw_record['SubmitterName'],
        },
        'caseworker': {
            'id': raw_record['CaseWorkerId'],
            'name': raw_record['CaseWorkerName'],
        },
        'pictures': []
    }

    for picture in raw_record['Pictures']:
        picture_dict = {
            'filename': picture['Filename'],
            'userid': picture['UserId'],
            'url': picture['Url'],
            'imagetype': picture['ImageType']
        }
        record['pictures'].append(picture_dict)

    return record

def convert_qd_category_int_to_text(value: int = 2) -> str:
    pass

def verify_record_type(record_type: str) -> bool:
    if record_type not in ['qd', 'rue']:
        raise ValueError(f'Unknown record_type: {record_type}')
    else:
        return True
    
def convert_date_to_smartdok_date_format(days_back: int) -> str:
    # Create a custom timezone with a specific offset (+01:00 in this case)
    custom_timezone = timezone(timedelta(hours=1))

    # Set the specific hour, minute, and second
    desired_time = datetime.time(13, 6, 9)

    # Get the current date in the custom timezone
    current_date = datetime.datetime.now(custom_timezone).date()

    # Combine the current date with the desired time to create the current datetime
    current_datetime = datetime.datetime.combine(current_date, desired_time)

    # Format today's date with timezone offset
    today_date = current_datetime.replace(microsecond=0).isoformat() + '+01:00'

    # Calculate date N days back with timezone offset
    days_back_date = (current_datetime - datetime.timedelta(days=days_back)).replace(microsecond=0).isoformat() + '+01:00'

    return today_date, days_back_date

def verify_init_params(username: str = None, password: str = None, user_agent: str = None) -> bool:
    if username == None:
        raise ValueError('username is None')
    if password == None:
        raise ValueError('password is None')
    if user_agent == None:
        raise ValueError('user_agent is None')
    else:
        logging.debug(f'verify_init_params - username={username}, password={password}, user_agent={user_agent}')

    return True
