import os
from dotenv import load_dotenv
import requests
import cv2

from config import IMAGES_FOLDER


def getImages(foldername = ''):
    images = os.listdir(IMAGES_FOLDER + foldername)
    return [image for image in images if image.endswith(".jpeg")]

def makeVideo():
    images = getImages()
    # create video using images in python, give code 
    image_folder = IMAGES_FOLDER
    video_name = 'video.avi'

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_name, fourcc, 1, (width,height))

    for image in images:
        image = cv2.imread(os.path.join(image_folder, image))
        image = cv2.resize(image, (width, height))
        video.write(image)

    cv2.destroyAllWindows()
    video.release()
    


if __name__ == "__main__":
    makeVideo()




