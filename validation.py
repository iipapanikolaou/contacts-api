import re

JSON_ATTRIBUTES = ['name', 'number']
ACCEPTABLE_QUERY_ARGUMENTS = ['page','limit','search','number']

class ValidationError(Exception):
    pass

def validate_data(data,request_method):
    if request_method == 'POST':

        for attribute in JSON_ATTRIBUTES:
            if attribute not in data:
                raise ValidationError(f"Field:{attribute}. Error: Required field.")

        if not name_is_valid(data['name']):
            raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))

        if not number_is_valid(data['number']):
            raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    elif request_method == 'PUT':

        acceptable_args_in_request = [key for key in data.keys() if key in JSON_ATTRIBUTES]
        if not acceptable_args_in_request:
            raise ValidationError("Missing required fields.")

        if data.get('name') is not None:
            if not name_is_valid(data.get('name')):
                raise ValidationError(invalid_format_msg('name','[A-Za-z] and whitespace','1-100'))

        if data.get('number') is not None:
            if not number_is_valid(data.get('number')):
                raise ValidationError(invalid_format_msg('number','[0-9]','7-15'))

    return data

def name_is_valid(name):

    if len(name) < 1 or len(name) > 100:
        return False

    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def number_is_valid(number):

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
        raise ValidationError('Pagination arguments should be non-zero, non-negative integers')
    
    return

def validate_arguments (arguments:list) -> None:

    for arg in arguments:

        try:
            if str(arg).lower() not in ACCEPTABLE_QUERY_ARGUMENTS:
                raise ValidationError("Query includes one or more unknown parameters.")
        except TypeError: # a query parameter includes characters outside of [A-Za-z]
            raise ValidationError("Invalid query parameters")
    
    return