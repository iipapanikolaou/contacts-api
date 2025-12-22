import re

JSON_ATTRIBUTES = ['name', 'number']

class ValidationError(Exception):
    pass

def validate_data(data,request_method):
    if request_method == 'POST':

        for attribute in JSON_ATTRIBUTES:
            if attribute not in data:
                raise ValidationError(f"Field:{attribute}. Error: Required field.")

        if not name_is_valid(data['name']):
            raise ValidationError("Field: name. Error: Invalid format. Acceptable characters: [A-Za-z] and whitespace. Acceptable length: 1-100 characters.")

        if not number_is_valid(data['number']):
            raise ValidationError("Field: number. Error: Invalid format. Acceptable characters: [0-9]. Acceptable length: 7-15 digits.")

    elif request_method == 'PUT':

        args_found = [key for key in data.keys() if key in JSON_ATTRIBUTES]
        if not args_found:
            raise ValidationError("Missing required fields.")


        if data.get('name') is not None:
            if not name_is_valid(data.get('name')):
                raise ValidationError("Field: name. Error: Invalid format. Acceptable characters: [A-Za-z] and whitespace. Acceptable length: 1-100 characters.")

        if data.get('number') is not None:
            if not number_is_valid(data.get('number')):
                raise ValidationError("Field: number. Error: Invalid format. Acceptable characters: [0-9]. Acceptable length: 7-15 digits.")

    return data

def name_is_valid(name):

    if len(name) < 1 or len(name) > 100:
        return False

    return bool(re.match(r'^[A-Za-z\s]+$', name.strip()))

def number_is_valid(number):

    if len(number) < 7 or len(number) > 15:
        return False

    return bool(re.match(r'^\d+$', number))