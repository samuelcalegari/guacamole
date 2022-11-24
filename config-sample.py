config = {
    'ldap': {
        'server': '',  # LDAP server
        'base': '',  # dc=mycompany,dc=en
        'filter': '',  # (&(departmentNumber=SALES)(enabled=TRUE))
        'userid_field': 'uid',  # uid
        'lastname_field': 'sn',  # sn
        'firstname_field': '',  # givenName
        'email_field': '',  # mail
    },
    'guacamole': {
        'server': '',  # Guacamole server
        'group': '',  # Specific group must be created in guacamole before
        # Used for LDAP synchronisation
        'group_always_on_users': '',  # Specific group must be created in guacamole before
        # Optional, used by tool auth-user.py
        'activation_mode': '',  # Activation mode : global or date
        'remaining_user_action': ''  # delete, disable, none
    },
    'moodle': {
        'api_end_point': '',
        # Moodle API End Point used in cron-moodle.py,
        # which returns users list in JSON format such as below,
        # needs specific plugin installed in Moodle (mod_guacamole)
    },
}

''' 
{
    "cnx": [
        {
            "user": "sdudent1",
            "timeopen": 1651132800,
            "timeclose": 1651140000
        },
        {
            "user": "sdudent2",
            "timeopen": 1651132800,
            "timeclose": 1651140000
        },
        ...
    ]
}
'''