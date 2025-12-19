# GET    - /contacts - list contacts
# GET    - /contacts/<id> - list specific contact
# POST   - /contacts - add contact
# PUT    - /contacts/<id> - edit contact
# DELETE - /contacts/<id> - delete contact

from flask import Flask, request, jsonify, abort
from database import init_db,get_contact_by_id,create_contact, update_contact,delete_contact,get_contacts,count_contacts

app = Flask(__name__)

if not init_db():
    abort(500)

# contacts = [
#     {"id": 1, "name": "john", "number": "6985699842"},
#     {"id": 2, "name": "adam", "number": "6985239842"},
#     {"id": 3, "name": "peter", "number": "6985645842"},
# ]

def errorResponse(errMsg: str,errCode: int):

    response = {
        "success": False,
        "data": None,
        "error": {"message": errMsg, "code": errCode},
    }

    return response

def success_response(data=None):
    return {
        "success": True,
        "data": data,
        "error": None
    }

def paginated_response(items, page:int, limit:int, total:int):
    return success_response({
        "items": items,
        "page": page,
        "limit": limit,
        "total": total
    })


@app.errorhandler(404)
def resource_not_found(e):

    response = errorResponse("SourceNotFound", 404)

    return jsonify(response), 404


@app.errorhandler(405)
def invalid_request(e):

    response = errorResponse("InvalidRequest", 405)

    return jsonify(response), 405


@app.errorhandler(400)
def bad_request(e):

    response = errorResponse("BadRequest", 400)

    return jsonify(response), 400


@app.errorhandler(500)
def internal_server_error(e):

    response = errorResponse("InternalServerError", 500)

    return jsonify(response), 500


# @app.errorhandler(Exception)
# def catch_unhandled_errors(e):

#     response = errorResponse(str(e),500)

#     return jsonify(response), 500


@app.get("/contacts")
def list_contacts():

    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
    except ValueError:
        abort(400)

    if page <= 0 or limit <= 0:
        abort(400)

    contactsRaw = get_contacts(page,limit)
    total = count_contacts()

    # Checks if pages before the requested page were sufficient enough to show all available data.
    # If they were, items key will display an empty list.
    # If page = 1, the condition will always be True
    if len(contactsRaw) == 0:

        response = paginated_response([],page,limit,total)
        return jsonify(response), 200
    
    contacts = list({'id':x[0],'name':x[1],'number':x[2]} for x in contactsRaw)
    response = paginated_response(contacts,page,limit,total)
    return jsonify(response), 200


@app.get("/contacts/<id>")
def list_contact(id):

    contactRaw = get_contact_by_id(id)

    if not contactRaw:
        abort(404)
    
    contact = {
        'id' : int(contactRaw[0]),
        'name' : contactRaw[1],
        'number' : contactRaw[2]
    }

    response = success_response(contact)

    return jsonify(response), 200


@app.post("/contacts")
def add_contact():
    payload = request.get_json(silent=True)

    if not payload:
        abort(400)

    contactName = payload.get("name")
    contactNumber = payload.get("number")

    if contactName and contactNumber:
        
        contactRaw = create_contact(contactName,contactNumber)

        if not contactRaw:
            abort(500)
        
        newContact = {
            'id' : int(contactRaw[0]),
            'name' : contactRaw[1],
            'number' : contactRaw[2]
        }

        response = success_response(newContact)

        return jsonify(response), 201
    
    abort(400)


@app.put("/contacts/<id>")
def edit_contact(id):

    payload = request.get_json(silent=True)

    if not payload:
        abort(400)

    contact = get_contact_by_id(id)

    if not contact:
        abort(404)

    contactName = payload.get("name") if payload.get("name") else contact[1]
    contactNumber = payload.get("number") if payload.get("number") else contact[2]

    app.logger.debug(f'prin ton elegxo')
    contactRaw = update_contact(id,contactName,contactNumber)
    app.logger.debug(f'update_contact::{contactRaw}')

    if not contactRaw:
        abort(500)
    
    newContact = {
        'id' : int(contactRaw[0]),
        'name' : contactRaw[1],
        'number' : contactRaw[2]
    }

    response = success_response(newContact)

    return jsonify(response), 201

@app.delete("/contacts/id")
def delete_contact(id):

    contact = get_contact_by_id(id)

    if not contact:
        abort(404)

    if not delete_contact(id):
        abort(500)
    
    return ("", 204)
    
app.run(debug=True)