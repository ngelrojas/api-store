import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from db import db

from blocklist import BLOCKLIST

from resources.item import blp as item_blue_print
from resources.store import blp as store_blue_print
from resources.tag import blp as tag_blue_print
from resources.user import blp as user_blu_print


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "rednodes"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "the token has been revoded.",
                    "error": "token_revoked. "
                }
            )
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify(
                {
                    "description": "the token is not fresh.",
                    "error": "fresh_token_required"
                }
            )
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        """
        - just example
        - look in the database and see whether the user is an admin
        """
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
                jsonify({"message": "the token has expired.", "error": "token_expired"}),
                401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({"message": "signature verification failed.", "error": "invalid_token"}),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify(
                {
                    "description": "request dows not contain an access token.",
                     "error": "authorization_required"
                }
            )
        )

    # with app.app_context():
    #     db.create_all()

    api.register_blueprint(item_blue_print)
    api.register_blueprint(store_blue_print)
    api.register_blueprint(tag_blue_print)
    api.register_blueprint(user_blu_print)

    # if __name__ == "__main__":
    #     app.run(host='0.0.0.0', port=5001, debug=True)

    return app

