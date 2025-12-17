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


@app.errorhandler(Exception)
def catch_unhandled_errors(e):

    response = errorResponse('InternalServerError',500)

    return jsonify(response), 500


@app.get("/contacts")
def list_contacts():

    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 5))
    except ValueError:
        abort(400)

    if page <= 0 or limit <= 0:
        abort(400)


    page = int(page)
    limit = int(limit)
    total = len(contacts)

    # Checks if pages before the requested page were sufficient enough to show all available data.
    # If they were, items key will display an empty list.
    # If page = 1, the condition will always be True
    if (page - 1) * limit >= total:

        data = {"items": [], "page": page, "limit": limit, "total": total}

        response = successResponse()
        response["data"] = data

        return jsonify(response), 200
    

    startIndex = (page - 1) * limit
    endIndex = startIndex + limit if startIndex + limit <= total else total

    subcontacts = contacts[startIndex:endIndex]
    items=[]
    for contact in subcontacts:
        items.append(contact)

    data = {"items": items, "page": page, "limit": limit, "total": total}

    response = successResponse()
    response['data']=data

    return jsonify(response), 200


@app.get("/contacts/<int:id>")
def list_contact(id):

    for contact in contacts:
        if contact["id"] == id:

            response = successResponse()
            response["data"] = contact

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
        response["data"] = newContact

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

            response = successResponse()
            response["data"] = contact

            return jsonify(response), 200

    abort(404)


@app.delete("/contacts/<int:id>")
def delete_contact(id):

    for contact in contacts:
        if contact["id"] == id:
            contacts.remove(contact)
            return ("", 204)

    abort(404)


app.run(debug=True)
