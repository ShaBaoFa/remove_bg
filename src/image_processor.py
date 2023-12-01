# Import necessary libraries
from PIL import Image, ImageTk
import io
import requests
from dotenv import dotenv_values
from removebg import RemoveBg
from cloud_service import CloudService


class ImageProcessor:
    def __init__(self):
        self.remove_bg_api_key = dotenv_values(".env")['REMOVE_BG_API_KEY']
        self.remove_bg_client = RemoveBg(self.remove_bg_api_key, "error.log")
        self.selected_color = None
    # Additional image processing methods can be added here
    def show_image(self, url, image_label):
        """
        Fetches an image from a URL and displays it on a given label widget.

        :param url: URL of the image to be displayed.
        :param image_label: Tkinter Label widget where the image will be displayed.
        """
        response = requests.get(url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image

    def remove_bg(self, url):
        """
        :param url: 文件地址
        :return:
        """
        try:
            print(f"正在去除背景: {url}")
            print(f"颜色选项: {self.selected_color}")
            self.remove_bg_client.remove_background_from_img_url(url, bg_color=self.selected_color)
        except Exception as e:
            raise Exception(f"去除背景失败: {e}")
