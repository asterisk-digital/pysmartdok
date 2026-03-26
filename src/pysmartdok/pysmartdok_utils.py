from datetime import timezone, timedelta
import datetime
import logging

from bs4 import BeautifulSoup
import requests


def soup_find_input_value(soup: BeautifulSoup = None, input_name: str = None) -> str:
    """
    soup_find_input_value is a static method that is used to find the value of an input element in a BeautifulSoup object.

    args:
        soup (BeautifulSoup): the BeautifulSoup object to search in.
        input_name (str): the name attribute of the input element to find.

    returns:
        str: the value of the found input element.
    """
    input = soup.find('input', attrs={'name': input_name})

    if input is None:
        raise Exception(f'no input found with name {input_name}')

    input_value = input['value']
    
    logging.debug(f'soup_find_input_value - name={input_name}, value={input_value}')

    return input_value

def dict_with_dict_to_dict(input_dict: dict = None) -> dict:
    """
    converts a dictionary with nested dictionaries to a flat dictionary.

    args:
        input_dict (dict): the input dictionary with nested dictionaries.

    returns:
        dict: the resulting flat dictionary.
    """
    output_dict = {}

    for key in input_dict:
        return_key = input_dict[key]['key']
        output_dict[return_key]= input_dict[key]['value']
        
    logging.debug(f'dict_with_dict_to_dict - from {input_dict} \n to {output_dict}')
        
    return output_dict

def convert_smartdok_rue_record_to_dict(raw_record: dict = None) -> dict:
    # TODO: implement this function
    # dident implement this function because we dont use the api to get rue records.
    return NotImplementedError(f'this isent implemented yet - raw_record={raw_record} was not converted to a dict')

def convert_smartdok_qd_record_to_dict(raw_record: dict = None) -> dict:
    # qd = quality deviation
    """
    convert a SmartDok QD record from its raw format to a dictionary format.

    args:
        raw_record (dict): the raw SmartDok QD record.

    returns:
        dict: the converted SmartDok QD record in dictionary format.
    """
    record = {
        'recordtype': 'qd',
        'title': raw_record['Title'],
        'description': raw_record['Description'],
        'status': raw_record['Status'],
        'category': '',
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
            'imagetype': picture['ImageType'],
        }
        response = requests.get(picture['Url'])
        
        if response.status_code != 200:
            raise Exception(f'request status code {response.status_code} != 200')
        
        picture_dict['image_data'] = response.content
        record['pictures'].append(picture_dict)


    # the 'category' is not directly available in the 'raw_record'. Instead, it's derived from the 'Values' list in the 'raw_record'.
    # each category in 'Values' is a dictionary with 'Type' and 'Values'.
    # we construct a 'raw_category_dict' from the first item in 'Values', extracting 'Type' and 'Values'.
    # the function 'convert_qd_category_dict_to_text' is then used to convert this dictionary into a category text.
    # this category text is added to the 'record' dictionary.
    raw_category_dict = {
        'type': raw_record['Values'][0]['Type'] if raw_record['Values'][0]['Type'] else None,
        'id': raw_record['Values'][0]['Values'][0] if raw_record['Values'][0]['Values'] else None
    }

    record['category'] = convert_qd_category_dict_to_text(raw_record, raw_category_dict)

    return record

def convert_qd_category_dict_to_text(raw_record: dict = None, category_dict: dict = None) -> str:
    """
    converts a category dictionary to text based on the provided raw record.

    args:
        raw_record (dict): the raw record containing the definition.
        category_dict (dict): the category dictionary containing the type and id.

    returns:
        str: the converted text based on the category dictionary.

    """
    # in each raw record, the 'Definition' is a dictionary with 'Values'.
    # each value in 'Values' is a dictionary with 'Type' and 'Values'.
    # each value in 'Values' is a dictionary with 'Id' and 'Name'.
    # the 'Id' is the category id, and the 'Name' is the category text.

    # we loop through the 'Values' in 'Definition' and find the value with the same 'Type' as the 'Type' in the 'category_dict'.
    record_definition = raw_record['Definition']

    if category_dict['type'] is None or category_dict['id'] is None:
        return ''

    for value in record_definition['Values']:
        if value['Type'] == category_dict['type']:
            for value_item in value['Values']:
                if value_item['Id'] == category_dict['id']:
                    return value_item['Name']
                
    return ''
    
def convert_date_to_smartdok_date_format(days_back: int = None) -> (str, str):
    """
    converts the current date and a specified number of days back to the SmartDok date format.

    args:
        days_back (int, optional): the number of days to go back from the current date. Defaults to None.

    returns:
        tuple: a tuple containing two strings - today's date in the SmartDok date format and the date N days back in the SmartDok date format.
    """
    # create a custom timezone with a specific offset (+01:00 in this case)
    # this is necessary because the SmartDok API requires the timezone offset to be included in the date
    custom_timezone = timezone(timedelta(hours=1))

    # set the specific hour, minute, and second
    desired_time = datetime.time()

    # get the current date in the custom timezone
    current_date = datetime.datetime.now(custom_timezone).date()

    # combine the current date with the desired time to create the current datetime
    current_datetime = datetime.datetime.combine(current_date, desired_time)

    # format today's date with timezone offset
    today_date = current_datetime.replace(microsecond=0).isoformat() + '+01:00'

    # calculate date N days back with timezone offset
    days_back_date = (current_datetime - datetime.timedelta(days=days_back)).replace(microsecond=0).isoformat() + '+01:00'

    return today_date, days_back_date

def verify_init_params(username: str = None, password: str = None, user_agent: str = None) -> bool:
    """
    verify the initialization parameters.

    args:
        username (str): the username.
        password (str): the password.
        user_agent (str): the user agent.

    returns:
        bool: true if the parameters are valid.

    raises:
        ValueError: if any of the parameters is None.
    """
    if username is None:
        raise ValueError('username is None')
    if password is None:
        raise ValueError('password is None')
    if user_agent is None:
        raise ValueError('user_agent is None')
    else:
        logging.debug(f'verify_init_params - username={username}, password={password}, user_agent={user_agent}')

    return True

def verify_record_type(record_type: str = None) -> bool:
    """
    verify if the given record_type is valid.

    args:
        record_type (str): the record type to be verified.

    returns:
        bool: true if the record_type is valid, False otherwise.

    raises:
        ValueError: if the record_type is not 'qd' or 'rue'.

    """
    if record_type not in ['qd', 'rue']:
        raise ValueError(f'unknown record_type: {record_type}')
    else:
        return True

def verify_login(response: requests.Response = None) -> bool:
    """
    verify if the login was successful by checking the status code and the presence of a specific HTML element.

    args:
        website (requests.Response, optional): the response object from the login request. Defaults to None.

    returns:
        bool: true if the login was successful, False otherwise.

    raises:
        Exception: if the login was not successful (no span with id 'LabelCompanyName' found).
    """
    if response.status_code != 200:
        raise Exception(f'request status code {response.status_code} != 200')
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # span with id LabelCompanyName is only present when logged in successfully
    if soup.find('span', attrs={'id': 'LabelCompanyName'}) is None:
        raise Exception('no span with id LabelCompanyName found')
    else:
        return True
