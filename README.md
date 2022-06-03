# LDAP Synchronization for Apache Guacamole #

## Features ##

- Synchronize LDAP users in Apache Guacamole
- Enable users from a Moodle web service
- Kill all actives connections

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

## Version ##

Current Version : 1.2 (03062022)

## Licence ##

Released under the [MIT Licence](https://opensource.org/licenses/MIT)
