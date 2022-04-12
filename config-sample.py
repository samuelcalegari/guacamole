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
        'group': ''  # Specific group must be create in guacamole before
    },
}
