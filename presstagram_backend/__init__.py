import os
from pathlib import Path

import tomlkit
from flask import Flask, jsonify, send_from_directory

from .presstagram import Presstagram

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.toml")

config = tomlkit.parse(Path(CONFIG_PATH).read_text("utf-8"))
flask_config = config["flask"]
presstagram_config = config["presstagram"]

HEADERS_PATH = os.path.join(PROJECT_ROOT, presstagram_config["headers_path"])
BACKGROUND_IMAGE_PATH = os.path.join(
    PROJECT_ROOT, presstagram_config["background_image_path"]
)
POSTS_DIR = os.path.join(PROJECT_ROOT, presstagram_config["posts_dir"])

presstagram = Presstagram(
    HEADERS_PATH,
    BACKGROUND_IMAGE_PATH,
    POSTS_DIR,
)

app = Flask(__name__)


@app.route("/images/<filename>")
def serve_image(filename):
    return send_from_directory(POSTS_DIR, filename)


@app.route("/images")
def images():
    image_files = sorted(
        [image for image in os.listdir(POSTS_DIR) if image.endswith(".png")],
        reverse=True,
    )
    response = jsonify({"images": image_files})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/print/<image_name>")
def print_image(image_name):
    if image_name:
        presstagram.print_image(os.path.join(POSTS_DIR, image_name))
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "No image name provided"})


@app.route("/update")
def update():
    if presstagram.in_progress:
        return jsonify({"success": False, "in_progress": True})
    presstagram.update_posts(
        presstagram_config["hashtag"],
        presstagram_config["number_of_posts"],
        presstagram_config["image_quality"],
        presstagram_config["image_base_width"],
        tuple(presstagram_config["image_paste_coordinates"]),
    )
    return jsonify({"success": True})


def main():
    print(f"HEADERS_PATH: {HEADERS_PATH}")
    print(f"CONFIG_PATH: {CONFIG_PATH}")
    print(f"HEADERS_PATH: {HEADERS_PATH}")
    print(f"BACKGROUND_IMAGE_PATH: {BACKGROUND_IMAGE_PATH}")
    print(f"POSTS_DIR: {POSTS_DIR}")
    print({k: v for k, v in config.items()})

    with app.app_context():
        update()

    app.run(host=flask_config["host"], debug=flask_config["debug"], port=5000)
