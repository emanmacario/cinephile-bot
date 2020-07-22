import logging
import os
import requests
from pathlib import Path

# Set logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def save_image_from_url(filename, url):
    """
    Saves an image in JPG format locally given the image URL
    :param filename: filename to save image as (starting with forward slash '/')
    :param url: image URL
    :return: None
    """
    logger.info(f"Saving image from URL: {url}")
    request = requests.get(url)
    if request.status_code == 200:
        image_path = (Path(__file__).parent / f'../images{filename}').resolve()
        with open(image_path, 'wb') as f:
            f.write(request.content)


def delete_image(filename):
    """
    Deletes an image from the 'images' directory with filename 'filename'
    :param filename: image filename (starting with forward slash '/')
    :return: None
    """
    # Delete image
    image_path = (Path(__file__).parent / f'../images{filename}').resolve()
    if os.path.exists(image_path):
        os.remove(image_path)


def main():
    url = 'https://image.tmdb.org/t/p/original/vScen3pRHnbtlfNxErROpiM8ABm.jpg'
    base_path = Path(__file__).parent

    file_path = (base_path / '../images/sample_image.jpg').resolve()
    print(type(file_path))
    print(os.path.exists(file_path))

    # request = requests.get(url)
    # if request.status_code == 200:
    #     with open(file_path, 'wb') as f:
    #         f.write(request.content)






if __name__ == "__main__":
    main()
    #print(os.path.exists('/cinephilebot/images'))