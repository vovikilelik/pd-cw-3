from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service, auth_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):

    @auth_service.auth_required()
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200


@genre_ns.route('/<int:rid>')
class GenreView(Resource):

    @auth_service.auth_required()
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @auth_service.auth_required('admin')
    def post(self):
        req_json = request.json
        movie = genre_service.create(req_json)
        return "", 201, {"location": f"/genres/{movie.id}"}

    @auth_service.auth_required('admin')
    def put(self):
        req_json = request.json
        movie = genre_service.update(req_json)
        return "", 201, {"location": f"/genres/{movie.id}"}

    @auth_service.auth_required('admin')
    def delete(self):
        req_json = request.json
        genre_service.delete(req_json.id)
        return "", 204
