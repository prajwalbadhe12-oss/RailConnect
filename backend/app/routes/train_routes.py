from flask import Blueprint, jsonify, request

from app.services.train_service import (
    get_all_trains,
    get_train_by_id,
    search_trains
)


train_bp = Blueprint("trains", __name__, url_prefix="/api/v1")


@train_bp.route("/trains", methods=["GET"])
def get_trains():
    trains = get_all_trains()

    return jsonify({
        "status": "success",
        "data_type": "database",
        "message": "Railway data retrieved from database",
        "count": len(trains),
        "trains": trains
    }), 200


@train_bp.route("/trains/<train_id>", methods=["GET"])
def get_train(train_id):
    train = get_train_by_id(train_id)

    if train is None:
        return jsonify({
            "status": "error",
            "message": "Train not found"
        }), 404

    return jsonify({
        "status": "success",
        "data_type": "database",
        "train": train
    }), 200


@train_bp.route("/search", methods=["GET"])
def search():
    source = request.args.get("source")
    destination = request.args.get("destination")

    if not source or not destination:
        return jsonify({
            "status": "error",
            "message": "Source and destination are required"
        }), 400

    trains = search_trains(source, destination)

    return jsonify({
        "status": "success",
        "data_type": "database",
        "count": len(trains),
        "trains": trains
    }), 200