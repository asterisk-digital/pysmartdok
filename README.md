# pysmartdok

A Python library for SmartDok' API. Under active development.

# Usage

The library can be used as follows:

```
import pysmartdok


credentials = {
  'username': 'my_user',
  'password': 'my_password',
  'user_agent': 'my_user_agent'
}

# Creating a client
client = pylandax.Client(credentials)

# Getting data
result = client.get_all_deviation_data(deviation_type='qd', amount_of_deviations=0, days_back=0, pool_size=1)
# only deviation_type is required, the rest are optional
# amount_of_deviations: 0 = all, 1 = last, 2 = last two, etc. Default: 0
# days_back: 0 = all, 1 = last 24 hours, 2 = last 48 hours, etc. Default: 0
# pool_size: number of threads to use for fetching data. Default: 1 (no threading)

```
