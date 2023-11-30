import json
from bottle import *
import folderstructure
from exif_read import read_exif, write_metadata, read_metadata, search_metadata, sort_tags
import logging
import platform
import getpass

iptcinfo_logger = logging.getLogger('iptcinfo')
iptcinfo_logger.setLevel(logging.ERROR)


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/')

@route('/<filename:path>')
def send_static(filename):
    if dirPath in f'/{filename}':
        filename = f'/{filename}'
        return static_file(filename.replace(dirPath, ''), root=dirPath)
    else:
        return static_file(filename, root='static/')

@route('/')
def home():
    return template('index.tpl')

@route('/sort')
def sort_images():
    folderstructure.sort(dirPath)
    sort_tags(dirPath)
    redirect('/')

@route('/dirPath')
def change_dirPath():
    global dirPath
    return template('dirPath.tpl', dirPath = dirPath)

@route('/setPath', method='POST')
def upload():
    global dirPath
    data = request.json
    if data['path'][-1] == '/':
        dirPath = data['path']
    else:
        dirPath = data['path'] + '/'
    with open('path.txt', 'w') as file:
        file.write(str(base64.standard_b64encode(bytes(dirPath, 'UTF-8')), 'UTF-8'))
    


@route('/api/getPictureYears', method='POST')
def getPicturesYears():
    pictures = folderstructure.images(dirPath)
    years = []
    for picture in pictures:
        picture = str(picture).replace(dirPath,'')
        try:
            int(picture[0:4])
            years.append(picture[0:4])
        except:
            None
    response.body = json.dumps({'years':years})
    return response

@route('/api/getPicturesMonths', method='POST')
def getPicturesMonths():
    data = request.json
    pictures = folderstructure.images(dirPath + str(data['year']) + '/')
    months = []
    for picture in pictures:
        picture = str(picture).replace(dirPath + str(data['year']) + '/','')
        if picture[0:2] not in months:
            months.append(picture[0:2])
    response.body = json.dumps({'months':months})
    return response

@route('/api/getPicturesDay', method='POST')
def getPictures():
    values = request.json
    pictures = folderstructure.images(dirPath + str(values['year']) + '/' + str(values['month']) + '/')
    days = []
    for picture in pictures:
        picture = str(picture).replace(dirPath + str(values['year']) + '/' + str(values['month']) + '/', '')
        days.append(picture[0:2])
    response.body = json.dumps({'days':days})
    return response

@route('/api/tags_write', method='POST')
def write_tags():
    data = request.json
    keywords = sorted(data['keywords'].split(', '))
    keywords_str = []
    if keywords != []:
        for keyword in keywords:
            keywords_str.append(keyword.encode('UTF-8'))
    write_metadata(data['src'], keywords)
    folderstructure.delete_image_backup(dirPath)

@route('/api/tags_read', method='POST')
def read_tags():
    data = request.json
    keywords = sorted(read_metadata(data['src']))#.replace('/pictures/', dirPath)))
    if keywords == 'no keywords':
        response.body = json.dumps({'keywords':[]})
        return response
    else:
        response.body = json.dumps({'keywords':keywords})
        return response

@route('/api/tags_search', method='POST')
def search_tags():
    data = request.json
    dates, keywords = search_metadata(data['keywords'])
    response.body = json.dumps({'dates':dates, 'keywords':keywords})
    return response

@route('/api/sendData', method='POST')
def receive_date():
    global pictures
    global dirPath
    date = request.json
    try:
        received_year = date['year']
        received_month = date['month']
        received_day = date['day']
        dirPath_picture = f'{dirPath}{received_year}/{received_month}/{received_day}/'
        pictures = folderstructure.images(dirPath_picture)
        response.body = json.dumps({'bilder':pictures})
        return response
    except Exception as error:
        print('Error:', error)

@route('/api/getEXIF', method='POST')
def getEXIF():
    picture = request.json
    exif_data = read_exif(picture['exif'])
    for key in exif_data:
        if exif_data[key] == '':
            exif_data[key] = 'keine Angabe'
    response.body = json_dumps({'datetime':exif_data['DateTimeOriginal'],
                                'camera':f"{exif_data['Image Make']} {exif_data['Image Model']}",
                                'artist':exif_data['Image Artist'].title(), 
                                'copyright':exif_data['Image Copyright'],
                                'gps':exif_data['Image GPSInfo'],
                                'exposure':exif_data['ExposureTime'],
                                'fnum':exif_data['FNumber'],
                                'iso':exif_data['ISOSpeedRatings'],
                                'focal_length':exif_data['FocalLength']
                                })
    return response

@route('/api/bin', method = 'POST')
def delete():
    picture = request.json
    folderstructure.delete_picture(picture['src'])


def check_for_path():
    global dirPath
    with open('path.txt', 'r') as file:
        try:
            lines = [line.rstrip('\n') for line in file.readlines()]        
            dirPath = lines[0]
            if dirPath != '':
                return dirPath
        except:
            dirPath = platform.system()
            user = getpass.getuser()
            if dirPath == 'Darwin':
                dirPath = f'/Users/{user}/Pictures/'
            elif dirPath == 'Windows':
                dirPath = 'C:\\Users\\' + user + '\\Pictures\\'
            elif dirPath == 'Linux':
                dirPath = f'/home/{user}/Pictures/'

            with open('path.txt', 'w') as file:
                file.write(str(base64.standard_b64encode(bytes(dirPath, 'UTF-8')), 'UTF-8'))
    return dirPath
            

if __name__ == '__main__':
    check_for_path()
    with open('path.txt', 'r') as file:
        lines = [line.rstrip('\n') for line in file.readlines()]        
        dirPath = lines[0]
        dirPath = base64.standard_b64decode(dirPath).decode('UTF-8').replace('\n', '') 
    pictures = []
    folderstructure.sort(dirPath)
    sort_tags(dirPath)
    folderstructure.delete_image_backup(dirPath)
    run(debug=True, reloader=True)