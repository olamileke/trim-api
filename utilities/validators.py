from validate_email import validate_email
import re

def redirect_source(value):
    if value is not None and isinstance(value, str) is False:
        raise ValueError('specified source must be a string')

    return value

def shortened_link(value):
    if len(value) < 6 or len(value) > 10:
        raise ValueError('Invalid shortened link')

    return value
 
def url_group(value):
    if value is None or isinstance(int(value), int):
        return value

    raise ValueError('Invalid group')

def short_url(value):
    value = value.strip()
    if value == '':
        return value

    if len(value) < 3:
        raise ValueError('short url must be at least 3 characters')

    return value

def url(value):
    url_match = re.compile('.*http.*')

    if url_match.findall(value) is None:
        raise ValueError('invalid url')

    return value.lower()

def group_name(value):
    if len(value) < 5:
        raise ValueError('name must be at least 5 characters')
        
    return value

def email(value): 
    if validate_email(value) == False:
        raise ValueError('email address is not valid')

    return value

def password(value):
    if len(value) < 8:
        raise ValueError('password must be at least 8 characters')

    return value