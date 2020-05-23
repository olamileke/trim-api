from validate_email import validate_email

def email(value): 
    if validate_email(value) == False:
        raise ValueError('email address is not valid')

    return value

def password(value):
    if len(value) < 8:
        raise ValueError('password must be at least 8 characters')

    return value