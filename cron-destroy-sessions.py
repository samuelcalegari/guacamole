from guacapy import Guacamole
from credentials import credentials
from config import config

guacamole = Guacamole(config['guacamole']['server'], credentials['guacamole']['user'], credentials['guacamole']['pass'])


# Create additional method for Guacamole class
def kill_connection(self, payload, datasource=None):
    """
    Example payload:
    [{"op":"remove","path":"/{{activeConnectionIdentifier}}"}]
    """
    if not datasource:
        datasource = self.primary_datasource
    return self._Guacamole__auth_request(
        method="PATCH",
        url="{}/session/data/{}/activeConnections/".format(
            self.REST_API, datasource
        ),
        payload=payload,
        json_response=False,
    )


# Add method Guacamole class
guacamole.kill_connection = kill_connection

# Get actives connections
connections = guacamole.get_active_connections()

# Kill all actives connections
for connection in connections:
    payload = [
        {"op": "remove", "path": "/" + connection}
    ]
    guacamole.kill_connection(guacamole, payload)
