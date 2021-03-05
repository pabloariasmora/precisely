import os
import json
from botocore.vendored import requests

# Only executed on Cold Start
# Simple Caching
session = {}

if not os.environ.get('preciselyAPIKey'):
    raise Exception('Missing preciselyAPIKey env variable')

if not os.environ.get('preciselyAPISECRET'):
    raise Exception('Missing preciselyAPISECRET env variable')

url = os.environ.get('URL')
if not url:
    raise Exception('Missing URL env variable')

min_length_allowed = os.environ.get('MinLengthAllowed')
if not url:
    raise Exception('Missing MinLengthAllowed env variable')

min_length_allowed = int(min_length_allowed)


def format_error(error):
    response = {
        "statusCode": error['statusCode'],
        "headers": {
            "Content-Type": "text/plain"
        },
        "isBase64Encoded": False,
        "body": json.dumps(
            {
                'message': error['message']
            }
        )
    }
    return response


def retrieve_session():

    payload = {'grant_type': 'client_credentials'}
    session_url = "https://{}:{}@{}/oauth/token".format(
        os.environ['preciselyAPIKey'],
        os.environ['preciselyAPISECRET'],
        url
    )
    global session
    try:
        r = requests.post(session_url, data=payload)
        session = r.json()
    except Exception as e:
        print(e)
        # TODO
        # Wide Exception need to investigate possible errors from precicely API.
        return format_error({
            'statusCode': 503,
            'code': 503,
            'message': 'Unable to perform query in this moment please try again later'
        })

    # TODO
    # Improve to validate expiresIn, but documentations has no details over it.


def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    query_strings = event.get('queryStringParameters')
    if not query_strings:
        return format_error({
            'statusCode': 404,
            'message': 'Missing input_address query string parameters'
        })

    input_address = query_strings.get('input_address')
    if not input_address or len(input_address) < min_length_allowed:
        return format_error({
            'statusCode': 400,
            'message': 'There is a minimal length ({}) requirement for input_address'.format(min_length_allowed)
        })

    global session

    if not session:
        retrieve_session()

    headers = {"Authorization": "Bearer {}".format(session['access_token'])}
    # TODO
    # Hardcoded paramaters
    precisely_url = "https://{}/typeahead/v1/locations?searchText={}&latitude=31.968600&longitude=-99.901800"\
                    "&searchRadius=1000&searchRadiusUnit=miles&maxCandidates=10"\
                    "&matchOnAddressNumber=True&returnAdminAreasOnly=N&includeRangesDetails=Y"\
                    "&country=usa&areaName1=tx".format(url, input_address)

    # TODO
    # Validate that is already encoded
    location_results = requests.get(precisely_url, headers=headers).json()

    addresses = []

    for location in location_results['location']:
        ranges = location.get('ranges', [])
        # If address is an Apartment object should have ranges
        if len(ranges):
            for range in ranges:
                if range.get('units'):
                    for unit in range['units']:
                        addresses.append(
                            {
                                'Type': 'Apartment',
                                'Address': unit['formattedUnitAddress']
                            }
                        )
        else:
            addresses.append(
                {
                    'Type': 'SingleFamilyHome',
                    'Address': location['address']['formattedAddress']
                }
            )

    if not addresses:
        return format_error({
            'statusCode': 404,
            'message': 'No Match Found'
        })


    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': json.dumps(addresses, indent=2)
    }
