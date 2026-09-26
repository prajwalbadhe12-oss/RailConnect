import os
import socket

from flask import Blueprint, jsonify

server_bp = Blueprint("server", __name__)


@server_bp.route("/api/server-info", methods=["GET"])
def server_info():

    hostname = socket.gethostname()

    instance_id = os.getenv(
        "EC2_INSTANCE_ID",
        "LOCAL-DEVELOPMENT"
    )

    availability_zone = os.getenv(
        "AWS_AVAILABILITY_ZONE",
        "LOCAL"
    )

    return jsonify({
        "application": "RailConnect",
        "instance_id": instance_id,
        "hostname": hostname,
        "availability_zone": availability_zone,
        "status": "healthy"
    }), 200