# Import necessary libraries
from PIL import Image, ImageTk
import io
import requests


class ImageProcessor:
    def __init__(self):
        # Initialization code here, if any
        pass

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



