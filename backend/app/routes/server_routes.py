import socket
import urllib.request
import urllib.error

from flask import Blueprint, jsonify

server_bp = Blueprint("server", __name__)


def get_ec2_metadata(path):
    """
    Retrieve metadata from the EC2 Instance Metadata Service (IMDSv2).
    Returns None if the application is running outside EC2.
    """
    try:
        # Request an IMDSv2 token
        token_request = urllib.request.Request(
            "http://169.254.169.254/latest/api/token",
            method="PUT",
            headers={
                "X-aws-ec2-metadata-token-ttl-seconds": "21600"
            }
        )

        with urllib.request.urlopen(token_request, timeout=2) as response:
            token = response.read().decode("utf-8")

        # Request the required metadata using the token
        metadata_request = urllib.request.Request(
            f"http://169.254.169.254/latest/meta-data/{path}",
            headers={
                "X-aws-ec2-metadata-token": token
            }
        )

        with urllib.request.urlopen(metadata_request, timeout=2) as response:
            return response.read().decode("utf-8")

    except (urllib.error.URLError, TimeoutError, OSError):
        return None


@server_bp.route("/api/server-info", methods=["GET"])
def server_info():

    hostname = socket.gethostname()

    instance_id = get_ec2_metadata("instance-id")
    availability_zone = get_ec2_metadata("placement/availability-zone")

    if instance_id is None:
        instance_id = "LOCAL-DEVELOPMENT"

    if availability_zone is None:
        availability_zone = "LOCAL"

    return jsonify({
        "application": "RailConnect",
        "instance_id": instance_id,
        "hostname": hostname,
        "availability_zone": availability_zone,
        "status": "healthy"
    }), 200