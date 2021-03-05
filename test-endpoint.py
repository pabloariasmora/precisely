import requests

# TODO
# This somehow can be loaded from CDK output
url = 'https://56su9fe5r3.execute-api.us-west-2.amazonaws.com/prod/'

# TODO
#  Make a version without encoding since is already encoded
input_address = '6636%20AVENUE%20J'

test_url = "{}?input_address={}".format(url, input_address)
print(test_url)
r = requests.get(test_url)
print(r.json())

input_address = '6715%20Lu'
test_url = "{}?input_address={}".format(url, input_address)
print(test_url)
r = requests.get(test_url)
print(r.json())


input_address = '&'
test_url = "{}?input_address={}".format(url, input_address)
print(test_url)
r = requests.get(test_url)
print(r.json())

input_address = '1618%20Park'
test_url = "{}?input_address={}".format(url, input_address)
print(test_url)
r = requests.get(test_url)
print(r.json())

