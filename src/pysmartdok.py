from multiprocessing import Pool
import datetime

from bs4 import BeautifulSoup as bs
import requests


class Client:
    def __init__(self, username, password, user_agent, pool_size=1):
        """Initializes the client with:
        ------------------------------
        username = username for SmartDok
        password = password for SmartDok
        user_agent = user agent for requests
        pool_size = number of processes to run in parallel
        """

        self.session = requests.Session()
        self.username = username
        self.password = password
        self.base_url = 'https://web.smartdok.no/'
        self.web_api_url = 'https://smartapi.smartdok.no/'
        self.api_url = 'https://api.smartdok.no/'
        self.pool_size = pool_size

        auth_fields = self.get_auth_fields()
        login_page = self.session.post(self.base_url, data=auth_fields)

        auth_string = self.get_auth_string(login_page)
        self.token = self.get_token(auth_string)
        self.userid = self.get_userid(auth_string)

        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': user_agent,
            'Token': self.token,
            'UserId': self.userid
        }

    def get_all_deviation_data(self, deviation_type):
        """runs get_deviation with all deviations as input with multiprocessing
        ------------------------------
        deviation_type = type of deviation to get | rue = RUE, qd = quality-deviation"""
        deviations = self.get_deviations(deviation_type)

        with Pool(self.pool_size) as pool:
            result = pool.map(self.get_deviation, deviations)
        pool.join()

        return result

    def get_reports(self):
        """gets all reports from SmartDok
        ------------------------------
        returns a list of dicts with report data """

        ''' to specify the response model:
        Inline Model [
            Inline Model 1
        ]
        Inline Model 1 {
            Id (integer, optional, read only),
            FilledOutDate (string, optional, read only),
            FilledOutBy (string, optional, read only),
            FilledOutById (string, optional, read only),
            Subject (string, optional, read only),
            SerialNumber (integer, optional, read only),
            FormTemplateId (integer, optional, read only),
            ModuleType (integer, optional, read only) = ['1', '2'],
            MainSerialNumber (string, optional, read only),
            ProjectId (integer, optional, read only),
            SubProjectId (integer, optional, read only),
            MachineId (integer, optional, read only),
            LastUpdated (string, optional, read only)
        }'''

        response = self.session.get(f"{self.api_url}forms/v2", headers=self.headers)

        response = response.json()

        return response

    def get_report_pdf(self, report_id: int):
        """gets the pdf data for a report by id
        -----------------------------------
        report_id (int) = id of the report to get pdf data for """
        payload = {
            'Token': self.token,
            'UserId': self.userid,
            'fileName': f'Checklist_{report_id}.pdf',
            'formIds': [report_id],
            'includeHistory': True,
        }

        response = self.session.post(f"{self.web_api_url}/Form/GetFormsPdf/{report_id}",
                                     json=payload, headers=self.headers)

        return response.content

    def get_deviations(self, deviation_type, take_arg=10, days_back=0):
        """Gets all deviations from SmartDok including only id and type
        ------------------------------
        deviation_type = type of deviation to get | rue = RUE, qd = quality-deviation
        take_arg = number of deviations to fetch at once | (default = 10) | 10 = 10 deviations
        days_back = number of days back to fetch deviations from | (default = 0) | 0 = all deviations
                    1 = deviations from last 24 hours | 2 = deviations from last 48 hours | etc.
        """

        to_date = datetime.datetime.now().replace(microsecond=0)
        # +01:00 is the timezone in SmartDok
        timezone = '+01:00'
        if days_back == 0:
            from_date = ''
        else:
            from_date = f'{to_date - datetime.timedelta(days=days_back)}{timezone}'

        options = {
            # which status we ignore when fetching all deviations (line 55 to see other options)
            'HideStatus[]': '2',
            'FromDate': from_date,
            'ToDate': f'{to_date}{timezone}',
            'Take': take_arg,
        }

        deviations = []

        response = self.session.get(f'{self.web_api_url}/{deviation_type}/overview',
                                    params=options, headers=self.headers)

        deviation_data = response.json()['data']

        for deviation_id in deviation_data:
            new_deviation = {
                'id': deviation_id['Id'],
                'type': deviation_type
            }
            deviations.append(new_deviation)

        return deviations

    def get_deviation(self, base_deviation: dict):
        """get deviation data from SmartDok with the use of base_deviation"""

        params = {
            'id': base_deviation['id'],
            'getAccessRights': 'true',
            'newSeverityValuesCompliant': 'true',
        }

        response = self.session.get(f"{self.web_api_url}/{base_deviation['type']}/report",
                                    params=params, headers=self.headers)

        deviation = response.json()

        img_list = []

        for img_num in deviation['Pictures']:
            img = requests.get(img_num['Url'], timeout=60)
            img_data = img.content

            img_dict = {
                'Filename': img_num['Filename'],
                'ImageType': img_num['ImageType'],
                'Img': img_data
            }

            img_list.append(img_dict)

        deviation_data = {
            'Title': deviation['Title'],
            'Description': deviation['Description'],
            'SubmitterName': deviation['SubmitterName'],
            'ProjectNumber': deviation['ProjectNumber'],
            'Pictures': img_list,
        }
        if base_deviation['type'] == 'rue':
            deviation_data['EventId'] = deviation['EventId']
            deviation_data['Category'] = deviation['Values'][0]['Values'][0]['Name']
            deviation_data['SubCategory'] = deviation['Values'][1]['Values'][0]['Name']
            deviation_data['OwnerName'] = deviation['OwnerName']
            deviation_data['type'] = 'rue'
        elif base_deviation['type'] == 'qd':
            deviation_data['DeviationId'] = deviation['DeviationId']
            deviation_data['CaseWorkerName'] = deviation['CaseWorkerName']
            deviation_data['type'] = 'qd'

            # get category and subcategory id from deviation
            category_type = deviation['Values'][0]['Type']
            category_id = deviation['Values'][0]['Values'][0]
            subcategory_type = deviation['Values'][1]['Type']
            subcategory_id = []
            for subcategory in deviation['Values'][1]['Values']:
                subcategory_id.append(subcategory)

            # get category and subcategory names from id
            deviation_data['Category'] = self.get_qd_category(deviation, category_type, category_id)
            deviation_data['SubCategory'] = self.get_qd_category(deviation, subcategory_type, subcategory_id)

        return deviation_data

    def apply_deviation_status(self, deviation_id, deviation_type, status=2):
        """Applies deviation status to given deviation by id
        ------------------------------
        deviation_id = id of the deviation to apply status to
        deviation_type = type of deviation to apply status to | rue = RUE, qd = quality-deviation
        status = status to apply to deviation | (default = 2) | 0 = untreated 1 = open, 2 = closed, 3 = rejected
                returns a requests.Response object
        """

        params = {
            'id': deviation_id,
            'status': status,
        }

        response = self.session.post(f"{self.web_api_url}/{deviation_type}/change-status",
                                     params=params, headers=self.headers)
        return response

    @staticmethod
    def get_qd_category(deviations, category_type, category_id):
        """get_qd_category is used to get category and subcategory names from id"""
        test_if_list = isinstance(category_id, list)
        for types in deviations['Definition']['Values']:
            if types['Type'] == category_type:
                if test_if_list:
                    new_category_id = []
                    for ID in category_id:
                        for name in types['Values']:
                            if ID == name['Id']:
                                new_category_id.append(name['Name'])
                    return new_category_id
                else:
                    for name in types['Values']:
                        if category_id == name['Id']:
                            category_id = name['Name']
                            return category_id

    # all functions below are used to log in to SmartDok and get the required data to use the browser version of the API
    def get_auth_fields(self):
        """get get_auth_fields is just to scrape info and return as login data"""
        forgery_str = 'SmartDokLoginView$LoginSmartDok$__antiForgeryToken'
        viewstate_str = '__VIEWSTATE'
        eventvalidation_str = '__EVENTVALIDATION'

        soup = self.session.get(self.base_url)
        page = bs(soup.text, 'html.parser')

        forgery = page.find('input', attrs={'name': forgery_str})
        forgery = forgery['value']

        viewstate = page.find('input', attrs={'name': viewstate_str})
        viewstate = viewstate['value']

        eventvalidation = page.find('input', attrs={'name': eventvalidation_str})
        eventvalidation = eventvalidation['value']

        auth_fields = {
            viewstate_str: viewstate,
            eventvalidation_str: eventvalidation,
            'SmartDokLoginView$LoginSmartDok$UserName': self.username,
            'SmartDokLoginView$LoginSmartDok$Password': self.password,
            forgery_str: forgery,
            'SmartDokLoginView$LoginSmartDok$LoginButton': 'Logg inn'
        }

        return auth_fields

    @staticmethod
    def get_auth_string(login_page):
        """extract auth string from login_page"""
        page = login_page.text

        char_remove = ['\n', '\r', '\t', '\\']
        for char in char_remove:
            page = page.replace(char, '')

        split_text = page.split('{')

        auth_string = ''

        for text in split_text:
            if 'Token":' in text:
                auth_string = text

        return auth_string

    @staticmethod
    def get_token(auth_string):
        """gets Token value out of auth string"""
        text = auth_string.split(',')

        token = ''
        char_remove = ['"', 'Token:']

        for line in text:
            if '"Token"' in line:
                token = line

        for char in char_remove:
            token = token.replace(char, '')

        return token

    @staticmethod
    def get_userid(auth_string):
        """gets UserID value out of auth string"""
        text = auth_string.split(',')

        userid = ''
        char_remove = ['"', 'UserId:']

        for line in text:
            if '"UserId"' in line:
                userid = line

        for char in char_remove:
            userid = userid.replace(char, '')

        return userid
