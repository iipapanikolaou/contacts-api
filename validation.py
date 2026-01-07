import re

PAYLOAD_FIELDS = {'name', 'number'}
ACCEPTABLE_QUERY_ARGUMENTS = {'page','limit','search','number'}

class ValidationError(Exception):
    pass

def validate_data(data,request_method):

    data_keys = set(data.keys())

    if request_method == 'POST':

        if len(data_keys) != len(PAYLOAD_FIELDS):
            raise ValidationError("Invalid number of fields.")

        if not PAYLOAD_FIELDS.issubset(data_keys):
            raise ValidationError("Missing required fields.")

        if not name_is_valid(data['name']):
            raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))

        if not number_is_valid(data['number']):
            raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    elif request_method == 'PUT':

        if len(data_keys) > len(PAYLOAD_FIELDS):
            raise ValidationError("Invalid number of fields.")

        if not data_keys.issubset(PAYLOAD_FIELDS):
            raise ValidationError("Missing required fields.")

        if not name_is_valid(data.get('name')):
            raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))

        if not number_is_valid(data.get('number')):
            raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    return data

def name_is_valid(name):

    if name is None:
        return False

    if len(name) < 1 or len(name) > 100:
        return False

    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def number_is_valid(number):

    if number is None:
        return False

    if len(number) < 7 or len(number) > 15:
        return False

    return bool(re.match(r'^\d+$', number))

def invalid_format_msg(field:str,characters_group:str,length_range:str) -> str:

    return f'Field: {field}. Error: Invalid format. Acceptable characters: {characters_group}. Acceptable length: {length_range}.'

def validate_pagination_arguments(page,limit) -> None:
    try:
        page = int(page)
        limit = int(limit)
    except ValueError:
        raise ValidationError('Invalid pagination arguments.')
    
    if page <= 0 or limit <= 0:
        raise ValidationError('Pagination arguments should be positive integers')
    
    return

def validate_arguments (arguments:list) -> None:

    if not set(arguments).issubset(ACCEPTABLE_QUERY_ARGUMENTS):
        raise ValidationError("Request includes one or more unknown arguments.")