from flask import Flask, request, jsonify, abort

# GET    - /contacts - list contacts
# GET    - /contacts/<id> - list specific contact
# POST   - /contacts - add contact
# PUT    - /contacts/<id> - edit contact
# DELETE - /contacts/<id> - delete contact

app = Flask(__name__)

contacts = [
    {"id": 1, "name": "john", "number": "6985699842"},
    {"id": 2, "name": "adam", "number": "6985239842"},
    {"id": 3, "name": "peter", "number": "6985645842"},
]

def errorResponse(
    errMsg: str,
    errCode: int,
):
    
    response = {
        "success": False,
        "data": None,
        "error": {"message": errMsg, "code": errCode},
    }

    return response

def successResponse():

    response = {"success": True, "data": None, "error": None}

    return response

# def createResponse(
#     data: list | dict | None = None,
#     success: bool = True,
#     errMsg: str | None = None,
#     errCode: int | None = None,
# ):
    
#     #This function returns a JSON response based on given arguments.
#     #Usage examples:
#     #Success: createResponse(data = data)
#     #Failure: createResponse(success=False,errMsg='<short status message>',errCode = '<http status code>')
    
#     if not success:
#         response = {
#             "success": False,
#             "data": None,
#             "error": {"message": errMsg, "code": errCode},
#         }
#         return response
    
#     response = {"success": True, "data": {"items":data,"page":1,"limit":5,"total":total items}, "error": None}

#     if success:
#         response = {"success": True, "data": data, "error": None}
#     else:
#         response = {
#             "success": False,
#             "data": None,
#             "error": {"message": errMsg, "code": errCode},
#         }
    
#     return response


@app.errorhandler(404)
def resource_not_found(e):

    response = errorResponse('SourceNotFound',404)

    return jsonify(response), 404

@app.errorhandler(405)
def invalid_request(e):

    response = errorResponse('InvalidRequest',405)

    return jsonify(response), 405

@app.errorhandler(400)
def bad_request(e):

    response = errorResponse('BadRequest',400)

    return jsonify(response), 400

@app.errorhandler(500)
def internal_server_error(e):

    response = errorResponse('InternalServerError',500)

    return jsonify(response), 500

@app.errorhandler(Exception)
def catch_unhandled_errors(e):

    response = errorResponse('InternalServerError',500)

    return jsonify(response), 500

@app.get("/contacts")
def list_contacts(page, limit):

    totalContacts = contacts.count()

    start = (page -1) * 5
    end = start + limit - 1

    if end > totalContacts:
        abort(400)

    items=[]
    for contact in contacts:
        if contact['id'] >= start and contact['id'] <= end:
            items.append(contact)
    
    response=successResponse(bulk=True)
    response['data']['items'] = items
    response['data']['page'] = page
    response['data']['limit'] = limit
    response['data']['total'] = totalContacts

    return jsonify(response), 200


@app.get("/contacts/<int:id>")
def list_contact(id):

    for contact in contacts:
        if contact["id"] == id:

            response = successResponse()
            response['data'] = contact

            return jsonify(response), 200

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

        response = successResponse()
        response['data'] = newContact

        return jsonify(response), 201

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

            response= successResponse()
            response['data'] = contact

            return jsonify(response), 200

    abort(404)


@app.delete("/contacts/<int:id>")
def delete_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            return ('', 204)

    abort(404)


app.run(debug=True)
