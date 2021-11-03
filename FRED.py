from fredapi import Fred

fred = Fred(api_key='39fa3bd07f8f55540a93e075a5f97cc1')
data = fred.get_series('GDP')

print(data.tail())
