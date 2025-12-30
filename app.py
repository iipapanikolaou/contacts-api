# GET    - /contacts - list contacts
# GET    - /contacts/<id> - list specific contact
# POST   - /contacts - add contact
# PUT    - /contacts/<id> - edit contact
# DELETE - /contacts/<id> - delete contact

from flask import Flask, request, jsonify, abort
import database as db
from validation import validate_data, ValidationError,validate_pagination_arguments,validate_arguments

app = Flask(__name__)

db.init_db()

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

    response = errorResponse('SourceNotFound', 404)

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


@app.errorhandler(ValidationError)
def handle_validation_error(e):

    response = errorResponse(str(e), 400)

    return jsonify(response), 400

# @app.errorhandler(Exception)
# def catch_unhandled_errors(e):

#     response = errorResponse(str(e),500)

#     return jsonify(response), 500


@app.get("/contacts")
def list_contacts():

    request_arguments = request.args
    page = request_arguments.get("page", 1)
    limit = request_arguments.get("limit", 5)
    validate_pagination_arguments(page,limit)
    validate_arguments(request_arguments.keys())

    contacts = db.get_contacts(page,limit,request_arguments)
    total = db.count_contacts(page,limit,request_arguments)

    if len(contacts) == 0:

        response = paginated_response([],page,limit,total)
        return jsonify(response), 200

    response = paginated_response(contacts,page,limit,total)
    return jsonify(response), 200


@app.get("/contacts/<int:id>")
def list_contact(id):

    contact = db.get_contact_by_id(id)

    if not contact:
        abort(404)

    response = success_response(contact)

    return jsonify(response), 200


@app.post("/contacts")
def add_contact():
    payload = request.get_json(silent=True)

    validated_data = validate_data(payload, 'POST')

    createdContactId = db.create_contact(validated_data['name'], validated_data['number'])

    if not createdContactId:
        abort(500)

    createdContact = db.get_contact_by_id(createdContactId)

    response = success_response(createdContact)

    return jsonify(response), 201


@app.put("/contacts/<int:id>")
def edit_contact(id):

    contact = db.get_contact_by_id(id)

    if not contact:
        abort(404)

    payload = request.get_json(silent=True)

    validated_data = validate_data(payload, 'PUT')

    contactName = validated_data.get("name") if validated_data.get("name") else contact['name']
    contactNumber = validated_data.get("number") if validated_data.get("number") else contact['number']

    if not db.update_contact(id,contactName,contactNumber):
        abort(500)

    updatedContact = db.get_contact_by_id(id)

    response = success_response(updatedContact)

    return jsonify(response), 201

@app.delete("/contacts/<int:id>")
def delete_contact(id):

    contact = db.get_contact_by_id(id)

    if not contact:
        abort(404)

    if not db.remove_contact(id):
        abort(500)
    
    return ("", 204)
    
app.run(debug=True)