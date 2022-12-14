from flask import Flask, Response, request, make_response
import json
from columbia_student_resource import ColumbiaStudentResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.put("/contacts/<uni>")
def post_contact(uni):
    body = request.json
    ColumbiaStudentResource.update_by_key(uni, body)
    return get_contact_by_uni(uni)


@app.post("/contacts")
def put_contact():
    body = request.json
    try:
        ColumbiaStudentResource.insert_by_key(body)
    except:
        return Response("Insert Failure", status=404, content_type="text/plain")
    return get_contact_by_uni(body["uni"])


@app.delete("/contacts/<uni>")
def delete_contact(uni):
    ColumbiaStudentResource.delete_by_key(uni)
    return Response("Delete Success")


@app.get("/contacts")
def get_contact_by_template():
    params = request.args
    result = ColumbiaStudentResource.get_by_params(params)
    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/contacts/<uni>", methods=["GET"])
def get_contact_by_uni(uni):
    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)
