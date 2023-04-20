from ldap3 import Server, Connection, SAFE_SYNC
from guacapy import Guacamole
from credentials import credentials
from config import config
import secrets

# Get Existing Users From guacamole
guacamole = Guacamole(config['guacamole']['server'], credentials['guacamole']['user'], credentials['guacamole']['pass'])

guacamoleUsersName = guacamole.get_group_members(config['guacamole']['group'])
guacamoleAllUsersName = guacamole.get_users()

# LDAP Search
ldapServer = Server(config['ldap']['server'])

conn = Connection(ldapServer,
                  credentials['ldap']['user'],
                  credentials['ldap']['pass'],
                  client_strategy=SAFE_SYNC,
                  auto_bind=True)

status, result, response, _ = conn.search(config['ldap']['base'],
                                          config['ldap']['filter'],
                                          attributes=[config['ldap']['userid_field'],
                                                      config['ldap']['lastname_field'],
                                                      config['ldap']['firstname_field'],
                                                      config['ldap']['email_field']])
if status:

    total_entries = len(response)
    total_users_created = 0
    total_users_deleted = 0
    total_users_disabled = 0

    # Fetch users from LDAP
    for entry in response:
        username = entry['attributes'][config['ldap']['userid_field']][0] if (len(
            entry['attributes'][config['ldap']['userid_field']]) != 0) else ""
        email = entry['attributes'][config['ldap']['email_field']][0] if (len(
            entry['attributes'][config['ldap']['email_field']]) != 0) else ""
        firstname = entry['attributes'][config['ldap']['firstname_field']][0] if (len(
            entry['attributes'][config['ldap']['firstname_field']]) != 0) else ""
        lastname = entry['attributes'][config['ldap']['lastname_field']][0] if (len(
            entry['attributes'][config['ldap']['lastname_field']]) != 0) else ""

        if username not in guacamoleUsersName:
            # Prevent to add an existing user
            if username not in guacamoleAllUsersName:
                if username != "" and email != "" and firstname != "" and lastname != "":
                    # Create user
                    payload = {
                        "username": username,
                        "password": secrets.token_urlsafe(16),
                        "attributes": {
                            "guac-full-name": firstname + ' ' + lastname,
                            "guac-organization": "UPVD",
                            "guac-email-address": email,
                            "disabled": True,
                            "expired": "",
                            "access-window-start": "",
                            "access-window-end": "",
                            "valid-from": "",
                            "valid-until": "",
                            "timezone": "null"
                        }
                    }
                    try:
                        guacamole.add_user(payload)

                        # Add user to group
                        payload = [{"op": "add", "path": "/", "value": username}]
                        guacamole.edit_group_members(config['guacamole']['group'], payload)

                        total_users_created = total_users_created + 1
                        print('Utilisateur', username, 'crée')
                    except:
                        print('Utilisateur', username, 'non crée')
        else:
            # User in Guacamole exists : remove from list
            guacamoleUsersName.remove(username)

    # Delete or disable users who are in the list (user are in Guacamole, but not in LDAP anymore)
    if config['guacamole']['remaining_user_action'] == 'delete':
        for userName in guacamoleUsersName:
            guacamole.delete_user(userName)
            total_users_deleted = total_users_deleted + 1
            print('Utilisateur', userName, 'supprimé')

    if config['guacamole']['remaining_user_action'] == 'disable':
        for userName in guacamoleUsersName:
            u = guacamole.get_user(userName)
            attributes = u["attributes"]
            attributes["disabled"] = True

            payload = {
                "attributes": attributes,
            }

            guacamole.edit_user(userName, payload)

            total_users_disabled = total_users_disabled + 1
            print('Utilisateur', userName, 'désactivé')

    # Display Infos
    print('Total des entrées :', total_entries)
    print('Total des utilisateurs crées :', total_users_created)
    print('Total des utilisateurs supprimés :', total_users_deleted)
    print('Total des utilisateurs désactivés :', total_users_disabled)

else:

    print('Une erreur est survenue lors de la connexion au serveur LDAP')
