from flask import Flask,request,jsonify

app = Flask(__name__)

contacts = [
    {'id':1,'name':'john','number':'6985699842'},
    {'id':2,'name':'adam','number':'6985239842'},
    {'id':3,'name':'peter','number':'6985645842'},
]

#GET    - /contacts - list contacts
#GET    - /contacts/<id> - list specific contact
#POST   - /contacts - add contact
#PUT    - /contacts/<id> - edit contact
#DELETE - /contacts/<id> - delete contact

def successResponse(sucessMessage = None,data = None):
    successMsg = {
        'success': True,
        'message':sucessMessage,
        'data': data,
    }

    return successMsg

def errorResponse(errorMessage = 'Unexpected error',errorCode = 400):
    errorMsg = {
        'data': None,
        'error': {
            'message': errorMessage,
            'code': errorCode
        }
    }

    return errorMsg


@app.route('/')
def homepage():
    return '<h1>Hello there!</h1>'

@app.get('/contacts')
def list_contacts():
    return jsonify(successResponse(contacts))

@app.get('/contacts/<id>')
def list_contact(id):

    if not id.isdigit():
        return (jsonify(errorResponse('No matching record for requested id',400)),400)
    
    for contact in contacts:
        if contact['id'] == int(id):
            return jsonify(successResponse(contact))
        
    return (jsonify(
        errorResponse('No matching record for requested id',400)),
        400
        )

@app.post('/contacts')
def add_contact():
    payload = request.get_json(silent=True)

    if not payload:
        return (jsonify(
        errorResponse('UnsupportedFormat.',400)),
        400
        )
    
    contactName = payload.get('name')
    contactNumber = payload.get('number')

    if contactName and contactNumber:
        newContact = {
            'id': max(int(c['id']) for c in contacts) + 1 if contacts else 1,
            'name': contactName,
            'number': contactNumber
        }

        contacts.append(newContact)

        return jsonify(successResponse('Contact added to the catalog',newContact))
    
    return (jsonify(
        errorResponse('InvalidSchema',400)),
        400
        )

@app.put('/contacts/<id>')
def edit_contact(id):

    if not id.isdigit():
        return (jsonify(errorResponse('No matching record for requested id',400)),400)

    payload = request.get_json(silent=True)

    if not payload:
        return (jsonify(
        errorResponse('UnsupportedFormat.',400)),
        400
        )

    contactName = payload.get('name')
    contactNumber = payload.get('number')

    for contact in contacts:
        if contact['id'] == int(id):
            contact['name'] = contactName if contactName else contact['name']
            contact['number'] = contactNumber if contactNumber else contact['number']
            
            return jsonify(successResponse('Contact changed',contact))
        
    return (jsonify(errorResponse('No matching record for requested id',400)),400)

@app.delete('/contacts/<id>')
def delete_contact(id):

    for contact in contacts:
        if contact['id'] == int(id):
            contacts.remove(contact)
            return jsonify(successResponse('Contact deleted',contact))
        
    return (jsonify(errorResponse('No matching record for requested id',400)),400)

app.run(debug=True)

