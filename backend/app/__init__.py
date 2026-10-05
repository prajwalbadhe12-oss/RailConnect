import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

from config.config import Config
from app.utils.logger import setup_logger


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # ---------------------------------
    # Application Logger
    # ---------------------------------

    logger = setup_logger()

    logger.info(
        "Starting RailConnect application"
    )

    logger.info(
        "Environment: %s",
        app.config["ENVIRONMENT"]
    )

    # ---------------------------------
    # CORS Configuration
    # ---------------------------------

    CORS(
        app,
        origins=app.config["CORS_ORIGINS"]
    )

    # ---------------------------------
    # Register Application Routes
    # ---------------------------------

    from app.routes.health_routes import health_bp
    from app.routes.server_routes import server_bp
    from app.routes.train_routes import train_bp
    from app.routes.booking_routes import booking_bp
    from app.routes.schedule_routes import schedule_bp
    from app.routes.seat_routes import seat_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(server_bp)
    app.register_blueprint(train_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(seat_bp)

    # ---------------------------------
    # Request Logging
    # ---------------------------------

    @app.before_request
    def log_request():

        request.start_time = __import__("time").perf_counter()

        logger.info(
            "Request started | method=%s | path=%s",
            request.method,
            request.path
        )

    @app.after_request
    def log_response(response):

        start_time = getattr(
            request,
            "start_time",
            None
        )

        if start_time is not None:
            elapsed_time = (
                __import__("time").perf_counter()
                - start_time
            )
        else:
            elapsed_time = 0

        logger.info(
            "Request completed | method=%s | path=%s | "
            "status=%s | duration_ms=%.2f",
            request.method,
            request.path,
            response.status_code,
            elapsed_time * 1000
        )

        return response

    # ---------------------------------
    # Global Error Handlers
    # ---------------------------------

    @app.errorhandler(400)
    def bad_request(error):

        logger.warning(
            "Bad request | path=%s | error=%s",
            request.path,
            error
        )

        return jsonify({
            "status": "error",
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):

        logger.warning(
            "Resource not found | path=%s | error=%s",
            request.path,
            error
        )

        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):

        logger.warning(
            "Method not allowed | method=%s | path=%s",
            request.method,
            request.path
        )

        return jsonify({
            "status": "error",
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):

        logger.error(
            "Internal server error | path=%s | error=%s",
            request.path,
            error
        )

        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    logger.info(
        "RailConnect application initialized successfully"
    )

    return app