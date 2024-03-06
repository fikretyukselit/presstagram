import os
from pathlib import Path
from pprint import pprint

import tomlkit
from flask import Flask, jsonify, send_from_directory

from .presstagram import Presstagram

PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.toml")

config = tomlkit.parse(Path(CONFIG_PATH).read_text("utf-8"))
flask_config = config["flask"]
presstagram_config = config["presstagram"]

headers_path = os.path.join(PROJECT_ROOT, presstagram_config["headers_path"])
background_image_path = os.path.join(
    PROJECT_ROOT, presstagram_config["background_image_path"]
)
posts_dir = os.path.join(PROJECT_ROOT, presstagram_config["posts_dir"])

presstagram_instance = Presstagram(
    headers_path,
    background_image_path,
    posts_dir,
)

app = Flask(__name__)


def enable_cors(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/images/<filename>")
def serve_image(filename):
    return enable_cors(send_from_directory(posts_dir, filename))


@app.route("/images")
def images():
    image_files = sorted(
        [image for image in os.listdir(posts_dir) if image.endswith(".png")],
        reverse=True,
    )
    return enable_cors(jsonify({"success": True, "images": image_files}))


@app.route("/print/<image_name>")
def print_image(image_name: str):
    if image_name:
        presstagram_instance.print_image(os.path.join(posts_dir, image_name))
        return enable_cors(jsonify({"success": True}))
    return enable_cors(jsonify({"success": False, "message": "no image name provided"}))


@app.route("/update_posts")
def update_posts():
    if presstagram_instance.in_progress:
        return enable_cors(jsonify({"success": False, "message": "in progress"}))
    presstagram_instance.update_posts(
        presstagram_config["hashtags"],
        presstagram_config["number_of_posts"],
        presstagram_config["image_quality"],
        presstagram_config["image_base_width"],
        tuple(presstagram_config["image_paste_coordinates"]),
    )
    return enable_cors(
        jsonify({"success": True, "message": "images updated from instagram"})
    )


@app.route("/config/reload")
def config_update():
    global config
    global presstagram_config
    config = tomlkit.parse(Path(CONFIG_PATH).read_text("utf-8"))
    presstagram_config = config["presstagram"]
    return enable_cors(jsonify({"success": True, "message": "config updated"}))


@app.route("/config/read")
def config_read():
    return enable_cors(jsonify({"success": True, "config": config}))


@app.route("/reload_presstagram")
def reload_presstagram():
    global presstagram_instance
    presstagram_instance_backup = presstagram_instance
    presstagram_instance = Presstagram(
        headers_path,
        background_image_path,
        posts_dir,
    )
    presstagram_instance.in_progress = presstagram_instance_backup.in_progress
    del presstagram_instance_backup
    return enable_cors(jsonify({"success": True, "message": "presstagram reloaded"}))


def main():
    print(f"CONFIG_PATH: {CONFIG_PATH}")
    print(f"HEADERS_PATH: {headers_path}")
    print(f"BACKGROUND_IMAGE_PATH: {background_image_path}")
    print(f"POSTS_DIR: {posts_dir}")
    pprint({k: v for k, v in config.items()})

    with app.app_context():
        update_posts()

    app.run(host="localhost", debug=flask_config["debug"], port=5000)


if __name__ == "__main__":
    main()
