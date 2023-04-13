# pysmartdok

A Python library for SmartDok' API. Under active development.

# Usage

The library can be used as follows:

```
import pysmartdok

# Credentials for SmartDok
# username and password is the same as for the web interface for SmartDok
credentials = {
  'username': 'my_user',
  'password': 'my_password',
  'user_agent': 'my_user_agent'
}

# Creating a client
client = pysmartdok.Client(username=credentials['username'], password=credentials['password'], user_agent=credentials['user_agent'])

# Getting data
result = client.get_all_deviation_data(deviation_type='qd', amount_of_deviations=0, days_back=0, pool_size=1)
"""only deviation_type is required, the rest are optional
deviation_type: 'qd' or 'rue' (quality-deviation or RUH ('rapport om uønsket hendelse'))
amount_of_deviations: 0 = all, 1 = last one, 2 = last two, etc. Default: 0
days_back: 0 = all, 1 = last 24 hours, 2 = last 48 hours, etc. Default: 0
pool_size: number of threads to use for fetching data. Default: 1 (no threading)
"""
```
