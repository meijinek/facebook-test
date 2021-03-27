import requests
import sys

account_id = sys.argv[1]
access_token = sys.argv[2]


def get_photos(account_id, access_token, after=None):
    #  after contains a query string with the next page
    if after:
        payload = {'type': 'uploaded', 'access_token': access_token, 'limit': '5', 'after': after}
    else:
        payload = {'type': 'uploaded', 'access_token': access_token, 'limit': '5'}

    try:
        x = requests.get(f'https://graph.facebook.com/v10.0/{account_id}/photos', params=payload)
    except:
        print('http request failed')

    photos = []

    #  if rate limit has been exceeded data will contain nought
    if x.json().get('data'):
        if len(x.json()['data']) > 0:
            for item in x.json()['data']:
                photos.append(str(item['id']))

    #  getting data from the next page recursively
    if x.json().get('paging'):
        photos.extend(get_photos(account_id, access_token, x.json()['paging']['cursors']['after']))

    return photos


my_facebook_photos = get_photos(account_id, access_token)

print(my_facebook_photos)
