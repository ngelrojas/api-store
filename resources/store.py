import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from schemas import StoreSchema
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from db import db

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        # store = StoreModel.query.get_or_404(store_id)
        return {"message", store_id}

    @jwt_required()
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "store deleted."}


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        _store = StoreModel(**store_data)
        try:
            db.session.add(_store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="a store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="an error occurred while inserting the store.")
        return _store
