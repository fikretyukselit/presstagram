import datetime
import json
import shutil
from pathlib import Path
import os

import requests

if os.name == "nt":
    import win32print
    import win32ui
    from PIL import Image, ImageWin
from PIL import Image


class Presstagram:
    def __init__(
        self,
        headers: str | Path | dict,
        background_path: str | Path,
        download_dir: str | Path,
    ) -> None:
        self.headers = (
            json.loads(Path(headers).read_text("utf-8"))
            if isinstance(headers, str) or isinstance(headers, Path)
            else headers
        )
        self.download_dir = (
            Path(download_dir) if isinstance(download_dir, str) else download_dir
        )
        self.background_path = (
            Path(background_path)
            if isinstance(background_path, str)
            else background_path
        )
        self.endpoint = (
            "https://www.instagram.com/api/v1/tags/logged_out_web_info/?tag_name={}"
        )
        self.in_progress = False

    def __sort_posts(self, posts: list | tuple) -> tuple:
        if isinstance(posts, tuple):
            return tuple(
                sorted(
                    posts,
                    key=lambda x: datetime.datetime.fromtimestamp(int(x[0])),
                    reverse=True,
                )
            )
        posts_list = [None] * len(posts)
        for i in range(len(posts)):
            node = posts[i]["node"]
            posts_list[i] = (
                str(node["taken_at_timestamp"]),
                str(node["id"]),
                str(node["display_url"]),
            )
        return tuple(
            sorted(
                posts_list,
                key=lambda x: datetime.datetime.fromtimestamp(int(x[0])),
                reverse=True,
            )
        )

    def __which_posts_to_have(
        self, fetched_posts: tuple, number_of_posts: int
    ) -> tuple:
        downloaded_posts = tuple(
            tuple(post.stem.split("-"))
            for post in self.download_dir.iterdir()
            if not (post.name.startswith(".") and not post.name.endswith(".png"))
        )

        def __custom_union(merge1: tuple | list, merge2: tuple | list) -> tuple:
            seen = set()
            union = []
            for item in merge1 + merge2:
                key = tuple(item[:2])
                if key not in seen:
                    seen.add(key)
                    union.append(item)
            return tuple(union)

        all_posts = __custom_union(downloaded_posts, fetched_posts)
        return self.__sort_posts(all_posts)[:number_of_posts]

    def __download_post(self, post: tuple) -> None:
        url = post[2]
        response = requests.get(url, stream=True)
        with open(self.download_dir / f"{post[0]}-{post[1]}.png", "wb") as file:
            shutil.copyfileobj(response.raw, file)
        del response

    def __edit_image(
        self, post: tuple, quality: int, base_width: int, paste_coordinates: tuple
    ) -> None:
        image = Image.open(self.download_dir / f"{post[0]}-{post[1]}.png").convert(
            "RGBA"
        )
        background = Image.open(self.background_path).convert("RGBA")
        wpercent = base_width / float(image.size[0])
        hsize = int((float(image.size[1]) * float(wpercent)))
        if hsize > base_width:
            image = image.resize((base_width, base_width + 1), Image.LANCZOS)
        else:
            image = image.resize((base_width, hsize), Image.LANCZOS)
        background.paste(image, paste_coordinates, image)
        background.save(
            self.download_dir / f"{post[0]}-{post[1]}.png",
            "PNG",
            optimize=True,
            quality=quality,
        )

    def __garbage_collector(self, posts_to_have: tuple) -> None:
        posts_to_have = tuple(tuple(post[:2]) for post in posts_to_have)
        for post in self.download_dir.iterdir():
            if not post.name.startswith("."):
                if tuple(post.stem.split("-")) not in posts_to_have:
                    post.unlink()
                    print(f"Deleted: {post.name}")

    def __get_recent_posts(self, hashtag: str) -> tuple:
        url = self.endpoint.format(hashtag)
        response = list(
            requests.get(url, headers=self.headers).json()["data"]["hashtag"][
                "edge_hashtag_to_media"
            ]["edges"]
        )
        result = self.__sort_posts(response)
        return result

    def update_posts(
        self,
        hashtag: str,
        number_of_posts: int,
        image_quality: int,
        image_base_width: int,
        image_paste_coordinates: tuple,
    ) -> None:
        self.in_progress = True
        posts_to_have = self.__which_posts_to_have(
            self.__get_recent_posts(hashtag), number_of_posts
        )
        for post in posts_to_have:
            if Path(self.download_dir / f"{post[0]}-{post[1]}.png").is_file():
                print(f"Already have: {post[0]}-{post[1]}.png")
                continue
            self.__download_post(post)
            self.__edit_image(
                post,
                quality=image_quality,
                base_width=image_base_width,
                paste_coordinates=image_paste_coordinates,
            )
            print(f"Downloaded: {post[0]}-{post[1]}.png")
        self.__garbage_collector(posts_to_have)
        self.in_progress = False

    def print_image(self, image_path: str) -> None:
        if os.name != "nt":
            print(f"Would print: {image_path}")
            return
        printer_name = win32print.GetDefaultPrinter()
        hDC = win32ui.CreateDC()
        hDC.CreatePrinterDC(printer_name)
        printer_size = hDC.GetDeviceCaps(110), hDC.GetDeviceCaps(111)
        bmp = Image.open(image_path)
        hDC.StartDoc(image_path)
        hDC.StartPage()
        dib = ImageWin.Dib(bmp)
        dib.draw(hDC.GetHandleOutput(), (0, 0, printer_size[0], printer_size[1]))
        hDC.EndPage()
        hDC.EndDoc()
        hDC.DeleteDC()
        
