import json
import requests
import time
from guacapy import Guacamole
from credentials import credentials
from config import config

guacamole = Guacamole(config['guacamole']['server'], credentials['guacamole']['user'], credentials['guacamole']['pass'])

request = requests.get(config['moodle']['api_end_point'] + "&wstoken=" + credentials['moodle']['api_token'])

if request.status_code == 200:

    try:
        data = json.loads(request.text)
        for entry in data['cnx']:
            user = entry['user']
            timeopen = entry['timeopen']
            timeclose = entry['timeclose']

            date_from = time.strftime('%Y-%m-%d', time.localtime(timeopen))
            time_from = time.strftime('%H:%M:%S', time.localtime(timeopen))
            date_until = time.strftime('%Y-%m-%d', time.localtime(timeclose))
            time_until = time.strftime('%H:%M:%S', time.localtime(timeclose))

            payload = {
                "attributes": {
                    "disabled": False,
                    "access-window-start": time_from,
                    "access-window-end": time_until,
                    "valid-from": date_from,
                    "valid-until": date_until,
                    "timezone": "Europe/Paris"
                },
            }

            # guacamole.edit_user(user, payload)
            print('Utilisateur', user, 'activé')

    except ValueError as e:
        print('Une erreur est survenue lors du décodage JSON')

else:
    print('Une erreur est survenue lors de la connexion au serveur web service moodle')
