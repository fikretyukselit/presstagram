# Presstagram

_Important Note: The actual printing functionality only works on Windows at the moment. It uses Windows-specific libraries and API to communicate with the printer. If you want to use the app on a different platform, please open a pull request and let us know how you did it._

Presstagram is a web app to be used at FIRST competitions and events. It automatically downloads the latest Instagram photos tagged with a specific event hashtag and frames them in a design made specifically for the event. The participants can then print the photos and take them home as a souvenir.

## Installation

Before we start, you need to have [Node.js](https://nodejs.org/en/) and [Python](https://www.python.org/) installed on your system. Then, you can clone the repository and install the dependencies:

```bash
git clone https://github.com/fikretyukselit/presstagram.git
cd presstagram
npm --prefix frontend install
pip install -r backend/requirements.txt
```

## Usage

To start the app, you need to run the frontend and the backend separately. First, start the backend (this may take some time if it's been a while since the last run):

```bash
python -m backend
```

Then, start the frontend in development mode:

```bash
npm --prefix frontend start
```

or build and serve the frontend for production:

```bash
npm --prefix frontend run build
npm install -g serve
serve -s frontend/build -l tcp://<host>:<port>
```

Note: Some ports may require administrative privileges to be used. If you encounter an error, try running the command as an administrator.

## Configuration

You can configure the app by editing the `config.toml` file. Here are the available options:

`[flask]`

- `debug`: {true, false} - Enable or disable debug mode.

`[presstagram]`

- `background_image_path`: string - Path to the background image.
- `posts_dir`: string - Path to the directory where the downloaded posts will be saved.
- `headers_path`: string - Path to the JSON file that contains the headers for fetching the posts.
- `hashtag`: string - The hashtag to search for.
- `number_of_posts`: integer - The number of posts to have in the machine. Older posts will be deleted when new posts are downloaded.
- `image_quality`: integer (1-100) - The quality of the images to be saved.
- `image_base_width`: integer (in pixels) - The width of the background's reserved space for the image to be pasted.
- `image_paste_coordinates`: [integer, integer] (in pixels) - The coordinates of the top-left corner where the image will be pasted. The images are scaled to fit the `image_base_width` and pasted to these coordinates.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Made with ❤️ by **Fikret Yüksel Foundation IT Committee**
