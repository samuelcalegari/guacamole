import getopt
import sys
from ldap3 import Server, Connection, SAFE_SYNC
from guacapy import Guacamole
from credentials import credentials
from config import config

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "ho:"

# Long options
long_options = ["Help", "Operation="]

# Variables
operation = ''
ldap_filter = ''
group = config['guacamole']['group_always_on_users']

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--Help"):
            print("Usage : auth-users.py -o [enable|disable] ['filter']")
            sys.exit()

        elif currentArgument in ("-o", "--Operation"):
            operation = currentValue

    if len(sys.argv) != 4:
        raise NameError('Missing arguments see: auth-users.py -h')

    if operation not in ['enable', 'disable']:
        raise NameError('Argument operation must be disable or enable')

    ldap_filter = sys.argv[3]

    # Guacamole
    guacamole = Guacamole(config['guacamole']['server'], credentials['guacamole']['user'],
                          credentials['guacamole']['pass'])

    available_groups = guacamole.get_user_groups()

    if group not in available_groups:
        raise NameError('Group ' + group + ' not found in Guacamole')

    # LDAP Search
    ldapServer = Server(config['ldap']['server'])

    conn = Connection(ldapServer,
                      credentials['ldap']['user'],
                      credentials['ldap']['pass'],
                      client_strategy=SAFE_SYNC,
                      auto_bind=True)

    status, result, response, _ = conn.search(config['ldap']['base'],
                                              ldap_filter,
                                              attributes=[config['ldap']['userid_field']])
    if status:

        # Fetch users from LDAP
        for entry in response:
            username = entry['attributes'][config['ldap']['userid_field']][0] if (len(
                entry['attributes'][config['ldap']['userid_field']]) != 0) else ""

            if operation == 'enable':

                # Add To Group
                payload = [
                    {"op": "add", "path": "/", "value": username}
                ]
                guacamole.edit_group_members(group, payload)

                # Remove From Group
                payload = [
                    {"op": "remove", "path": "/", "value": username}
                ]
                guacamole.edit_group_members(config['guacamole']['group'], payload)

                # Enable User
                u = guacamole.get_user(username)
                attributes = u["attributes"]
                attributes["disabled"] = False
                payload = {
                    "attributes": attributes,
                }

                guacamole.edit_user(username, payload)

            else:

                # Add To Group
                payload = [
                    {"op": "add", "path": "/", "value": username}
                ]
                guacamole.edit_group_members(config['guacamole']['group'], payload)

                # Remove From Group
                payload = [
                    {"op": "remove", "path": "/", "value": username}
                ]
                guacamole.edit_group_members(group, payload)

                # Disable User
                u = guacamole.get_user(username)
                attributes = u["attributes"]
                attributes["disabled"] = True
                payload = {
                    "attributes": attributes,
                }

                guacamole.edit_user(username, payload)

except (getopt.error, NameError) as err:
    # output error, and return with an error code
    print(str(err))
