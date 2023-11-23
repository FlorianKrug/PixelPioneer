import os
from PIL import Image
from datetime import datetime
import shutil
from exif_read import sort_tags

def sort(dirPath):
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    for picture in os.listdir(dirPath):
        if os.path.isfile(dirPath + picture) and picture != ".DS_Store" and picture.split(".")[-1] in endswith: #.DS_Store only important for apple devices
            img = Image.open(dirPath + picture)
            try:
                img_exif = img._getexif()[36867]
                if img_exif is not None:
                    move_files(img_exif, dirPath, picture)
                    sort_tags(dirPath)
            except:
                shutil.move(dirPath + picture, dirPath + "Fehler/")
            

def images(dirPath):
    images = []
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    for root, _, files in os.walk(dirPath):
        for file in files:
            if file == ".DS_Store":
                continue
            if "~" in file:
                continue
            if file.split(".")[-1].lower() in endswith:
                images.append(os.path.join(root, file))
    return images

def delete_picture(dirPath):
    os.remove(dirPath)

def move_files(img_exif, dirPath, picture):
    time = datetime.strptime(img_exif,'%Y:%m:%d %H:%M:%S')
    time.strftime('%a %d %b %Y, %I:%M%p')
    if not os.path.exists(dirPath + str(time.year) + "/"): #create folder if year doesn't exist
        os.mkdir(dirPath + str(time.year))
    if not os.path.exists(dirPath + str(time.year) + "/" + str(time.month)): #create folder if month doesn't exist
        os.mkdir(dirPath + str(time.year) + "/" + str(time.month))
    if not os.path.exists(dirPath + str(time.year) + "/" + str(time.month) + "/" + str(time.day)): #create folder if day doesn't exist
        os.mkdir(dirPath + str(time.year) + "/" + str(time.month) + "/" + str(time.day))
    shutil.move(dirPath + picture , dirPath + str(time.year) + "/" + str(time.month) + "/" + str(time.day) + "/")

def delete_image_backup(dirPath): #delete file with metadata backup
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            if file[-1] is "~":
                delete_picture(root + "/" + file)