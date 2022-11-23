# LDAP Synchronization for Apache Guacamole #

## Features ##

- Synchronize LDAP users in Apache Guacamole
- Enable users from a Moodle web service
- Kill all actives connections
- Enable / Disable users tool script

## Requirement ##

Python 3.8 or greater.

## Installation ##

    pip3 install -r requirements.txt

## Configuration ##

- Rename config-sample.py to config.py
- Rename credentials-sample.py to credentials.py
- Fill your information in these files

## Usage ##

    python3 main.py

## Moodle Cron ##

Add cron-moodle.py in crontab (every minute), witch permits to enable users from moodle

## Kill Connections Cron ##

Add cron-destroy-sessions.py in crontab (every day, ie 3 am), witch permits to kill all actives connections

## Enable / Disable users tool script ##

use auth-user.py script move users from initial group (users disabled by default) in config.py 
to another group (users already enabled)

    Usage: 
    python3 auth-users.py -o [enable|disable] ['filter'] ['group']

    Examples:
    python3 auth-users.py -o enable '(uid=jsmith)' 'Direct'
    python3 auth-users.py -o disable '(&(departmentNumber=SALES)(enabled=TRUE))' 'Direct'

## Version ##

Current Version : 1.3 (14112022)

## Licence ##

Released under the [MIT Licence](https://opensource.org/licenses/MIT)
