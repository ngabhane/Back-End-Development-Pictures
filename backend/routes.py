from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {'message': 'data not present'}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    res = None
    for info in data:
        currId = info.get('id')
        if currId == id:
            res = {'id': id, 'event_state': info.get('event_state')}
            break
    if res:
        return res, 200
    return {'message': 'url for requested id: %d not found'}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    pictureId = picture.get('id')
    for picInfo in data:
        if picInfo.get('id') == pictureId:
            return {'Message': "picture with id %d already present" % pictureId}, 302
    data.append(picture)
    return {'id': pictureId}, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    for i, pictureInfo in enumerate(data):
        if pictureInfo.get('id') == id:
            data[i] = picture
            return {}, 200
    return {'message': "picture not found"}


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    res = None
    for i, pictureInfo in enumerate(data):
        if id == pictureInfo.get('id'):
            res = i
            break
    if res is not None:
        del data[res]
        return {}, 204
    return {"message": "picture not found"}, 404
