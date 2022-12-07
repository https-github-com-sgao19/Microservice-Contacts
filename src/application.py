from flask import Flask, Response, request, make_response
from datetime import datetime
import json
from columbia_student_resource import ColumbiaStudentResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__)

CORS(app)


@app.route("/test", methods=["GET", "POST"])
def test_flask():
    if request.method == "POST":
        msg = {1: "test POST"}
        rsp = Response(json.dumps(msg), status=404, content_type="application/json")
    else:
        msg = {2: "test GET"}
        rsp = make_response(msg)
        rsp.status = 404
        rsp.headers['customHeader'] = 'This is a custom header'

    return rsp


@app.put("/contacts/<uni>")
def post_contact(uni):
    params = request.form
    ColumbiaStudentResource.update_by_key(uni, params)
    return get_contact_by_uni(uni)


@app.post("/contacts")
def put_contact():
    print("post")
    body = request.form
    print("post")
    print(body)
    try:
        ColumbiaStudentResource.insert_by_key(body)
    except:
        return Response("Insert Failure", status=404, content_type="text/plain")
    return get_contact_by_uni(body["uni"])


@app.delete("/contacts/<uni>")
def delete_contact(uni):
    ColumbiaStudentResource.delete_by_key(uni)
    return Response("Delete Success")


@app.get("/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "F22-Starter-Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result


@app.route("/contacts/<uni>", methods=["GET"])
def get_contact_by_uni(uni):

    result = ColumbiaStudentResource.get_by_key(uni)

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5012)
    # test visibility

