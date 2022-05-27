from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service, auth_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        page = request.args.get('page')

        rs = director_service.get_all(page=page, limit=12)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@director_ns.route('/<int:rid>')
class DirectorView(Resource):

    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @auth_service.auth_required()
    def post(self):
        req_json = request.json
        movie = director_service.create(req_json)
        return "", 201, {"location": f"/directors/{movie.id}"}

    @auth_service.auth_required()
    def put(self):
        req_json = request.json
        movie = director_service.update(req_json)
        return "", 201, {"location": f"/directors/{movie.id}"}

    @auth_service.auth_required()
    def delete(self):
        req_json = request.json
        director_service.delete(req_json.id)
        return "", 204
