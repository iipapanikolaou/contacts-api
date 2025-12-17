from flask import Flask, request, jsonify, abort

app = Flask(__name__)

contacts = [
    {"id": 1, "name": "john", "number": "6985699842"},
    {"id": 2, "name": "adam", "number": "6985239842"},
    {"id": 3, "name": "peter", "number": "6985645842"},
]

# GET    - /contacts - list contacts
# GET    - /contacts/<id> - list specific contact
# POST   - /contacts - add contact
# PUT    - /contacts/<id> - edit contact
# DELETE - /contacts/<id> - delete contact


def createResponse(
    data: list | dict | None = None,
    success: bool = True,
    errMsg: str | None = None,
    errCode: int | None = None,
):
    
    #This function returns a JSON response based on given arguments.
    #Usage examples:
    #Success: createResponse(data = data)
    #Failure: createResponse(success=False,errMsg='<short status message>',errCode = '<http status code>')
    

    if success:
        response = {"success": True, "data": data, "error": None}
    else:
        response = {
            "success": False,
            "data": None,
            "error": {"message": errMsg, "code": errCode},
        }
    
    return response


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(createResponse(success=False,errMsg='SourceNotFound',errCode = 404)),404

@app.errorhandler(405)
def invalid_request(e):
    return jsonify(createResponse(success=False,errMsg='InvalidRequest',errCode = 405)),405

@app.errorhandler(400)
def bad_request(e):
    return jsonify(createResponse(success=False,errMsg='BadRequest',errCode = 400)),400

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(createResponse(success=False,errMsg='InternalServerError',errCode = 500)),500


@app.get("/contacts")
def list_contacts():
    return jsonify(createResponse(data=contacts)), 200


@app.get("/contacts/<int:id>")
def list_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            return jsonify(createResponse(data=contact)), 200

    abort(404)


@app.post("/contacts")
def add_contact():
    payload = request.get_json(silent=True)

    if not payload:
        abort(400)

    contactName = payload.get("name")
    contactNumber = payload.get("number")

    if contactName and contactNumber:
        newContact = {
            "id": max(int(c["id"]) for c in contacts) + 1 if contacts else 1,
            "name": contactName,
            "number": contactNumber,
        }

        contacts.append(newContact)

        return jsonify(createResponse(data=newContact)), 201

    abort(400)


@app.put("/contacts/<int:id>")
def edit_contact(id):

    payload = request.get_json(silent=True)

    if not payload:
        abort(400)

    contactName = payload.get("name")
    contactNumber = payload.get("number")

    for contact in contacts:
        if contact["id"] == id:
            contact["name"] = contactName if contactName else contact["name"]
            contact["number"] = contactNumber if contactNumber else contact["number"]

            return jsonify(createResponse(data=contact)), 200

    abort(404)


@app.delete("/contacts/<int:id>")
def delete_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            return ("", 204)

    abort(404)


app.run(debug=True)
