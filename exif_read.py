import exifread
import iptcinfo3
import os

def read_exif(dirPath):
    exif_tags = ['EXIF DateTimeOriginal','Image Model', 'Image Make', 'Image Artist', 'Image Copyright', 'Image GPSInfo', 'EXIF ExposureTime', 'EXIF FNumber', 'EXIF ISOSpeedRatings', 'EXIF FocalLength']
    exif = {'DateTimeOriginal':'','Image Model':"", 'Image Make':'', 'Image Artist':'', 'Image Copyright':'', 'Image GPSInfo':'', 'ExposureTime':'', 'FNumber':'', 'ISOSpeedRatings':'', 'FocalLength':''}
    picture = open("static/" + dirPath, 'rb')
    tags = exifread.process_file(picture)
    for tag in tags.keys():
        if tag in exif_tags:
            value = str(tags[tag])
            if tag == "EXIF FocalLength" and "/" in value or tag == "EXIF FNumber" and "/" in value:
                new_value = value.split("/")
                value = int(new_value[0]) / int(new_value[1])
                value = str(value)
            exif.update({tag.replace('EXIF ', ''): value})
    return exif

def write_metadata(dirPath, keywords):
    info = iptcinfo3.IPTCInfo('static/' + dirPath)
    info['keywords'] = sorted(keywords)
    info.save(options=["overwrite"])

def read_metadata(dirPath):
    picture = iptcinfo3.IPTCInfo(dirPath)
    info = [x.lower().decode('UTF-8') for x in picture['keywords']]
    if info is []:
        return "no keywords"
    keywords = []
    for keyword in info:
        keywords.append(keyword)
    return keywords

def search_metadata(keywords):
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    picture_dates = []
    picture_keywords = []
    for root, _, files in os.walk('static/'):
        for file in files:
            for keyword in keywords:
                if file.split('.')[-1].lower() in endswith and file != ".DS_Store":
                    if keyword.lower() in read_metadata(root+"/"+file):
                        newroot = root.replace("static/Bilder/", "")
                        if f"{newroot[0:4]}.{newroot[5:7]}.{newroot[8:10]}" not in picture_dates:
                            picture_dates.append(f"{newroot[0:4]}.{newroot[5:7]}.{newroot[8:10]}")
                            picture_keywords.append(sorted(read_metadata(root+"/"+file)))
                        
    return picture_dates, picture_keywords

def sort_tags(dirPath):
    endswith = ["cr2", "jpg", "jpeg", "tiff", "tif", "nef", "arw", "png", "gif", "webp"]
    for root, _, files in os.walk(dirPath):
        for file in files:
            if os.path.isfile(root + "/" + file) and file != ".DS_Store" and file.split(".")[-1] in endswith:
                    picture = iptcinfo3.IPTCInfo(root + "/" + file)
                    info = picture ['keywords']
                    if info is []:
                        None
                    else:
                        picture['keywords'] = sorted(info)
                    