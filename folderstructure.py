import os
from PIL import Image
from datetime import datetime
import shutil
from exif_read import sort_tags

def sort(dirPath):
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    for picture in os.listdir(dirPath):
        if not os.path.isfile(dirPath + picture):
            continue
        if picture.split(".")[-1].lower() in endswith:
            img = Image.open(dirPath + picture)
            try:
                img_exif = img._getexif()[36867]
                if img_exif is not None:
                    move_files(img_exif, dirPath, picture)
                    sort_tags(dirPath)
            except TypeError:
                file_path = os.path.normpath(os.path.join(dirPath, 'Fehler/'))
                shutil.move(dirPath + picture, file_path)
            except SyntaxError as e:
                print(e)
            except KeyError as e:
                print('This file has no DatetimeOriginal:', dirPath + picture)
                print('Error:', e)
                file_path = os.path.normpath(os.path.join(dirPath, 'Fehler/'))
                shutil.move(dirPath + picture, file_path)
            

def images(dirPath):
    images = []
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    for root, _, files in os.walk(dirPath):
        for file in files:
            if "~" in file:
                continue
            if file.split(".")[-1].lower() in endswith:
                images.append(os.path.join(root, file))
    return images

def delete_picture(dirPath):
    os.remove(dirPath)

def move_files(img_exif, dirPath, picture):
    time = datetime.strptime(img_exif,'%Y:%m:%d %H:%M:%S')
    print(time.month)
    time.strftime('%a %d %b %Y, %I:%M%p')
    if time.month < 10:
        month = '0' + str(time.month)
    else:
        month = time.month
    if not os.path.exists(dirPath + str(time.year) + "/"): #create folder if year doesn't exist
        os.mkdir(dirPath + str(time.year))
    if not os.path.exists(dirPath + str(time.year) + "/" + month): #create folder if month doesn't exist
        os.mkdir(dirPath + str(time.year) + "/" + month)
    if not os.path.exists(dirPath + str(time.year) + "/" + month + "/" + str(time.day)): #create folder if day doesn't exist
        os.mkdir(dirPath + str(time.year) + "/" + month + "/" + str(time.day))
    shutil.move(dirPath + picture , dirPath + str(time.year) + "/" + month + "/" + str(time.day) + "/")

def delete_image_backup(dirPath): #delete file with metadata backup
    for root, dirs, files in os.walk(dirPath):
        for file in files:
            if file[-1] == "~":
                delete_picture(root + "/" + file)