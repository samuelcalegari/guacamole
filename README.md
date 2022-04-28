# LDAP Synchronization for Apache Guacamole #

## Current version ##

1.0

## Features ##

- Synchronize LDAP users in Apache Guacamole
- Enable users from a Moodle web service

## Installation ##

    pip3 install -r requirements.txt

## Configuration ##

- Rename config-sample.py to config.py
- Rename credentials-sample.py to credentials.py
- Fill your information in these files

## Launch ##

    python3 main.py

## Requirement ##

Python 3.8 or greater.

## Moodle Cron ##

Add cron-moodle.py in crontab (every minute), witch permits to enable users from moodle

## Licence ##

Released under the [MIT Licence](https://opensource.org/licenses/MIT)
