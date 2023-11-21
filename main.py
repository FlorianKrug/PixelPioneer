import json
from bottle import *
import folderstructure
from exif_read import read_exif, write_metadata, read_metadata, search_metadata, sort_tags
import logging

iptcinfo_logger = logging.getLogger('iptcinfo')
iptcinfo_logger.setLevel(logging.ERROR)

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/')

@route('/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static/')

@route('/')
def home():
    return template('index.tpl')

@route('/sort')
def sort_images():
    folderstructure.sort('static/Bilder/')
    sort_tags('static/Bilder/')
    redirect('/')

@route('/api/getPictureYears', method='POST')
def getPicturesYears():
    pictures = folderstructure.images('static/Bilder/')
    years = []
    for picture in pictures:
        picture = str(picture).replace('static/Bilder/','')
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
    pictures = folderstructure.images('static/Bilder/' + str(data['year']) + '/')
    months = []
    for picture in pictures:
        picture = str(picture).replace('static/Bilder/' + str(data['year']) + '/','')
        if picture[0:2] not in months:
            months.append(picture[0:2])
    response.body = json.dumps({'months':months})
    return response

@route('/api/getPicturesDay', method='POST')
def getPictures():
    values = request.json
    pictures = folderstructure.images('static/Bilder/' + str(values['year']) + '/' + str(values['month']) + '/')
    days = []
    for picture in pictures:
        picture = str(picture).replace('static/Bilder/' + str(values['year']) + '/' + str(values['month']) + '/', '')
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
    folderstructure.delete_image_backup('static/Bilder/')

@route('/api/tags_read', method='POST')
def read_tags():
    data = request.json
    keywords = sorted(read_metadata('static/' +  data['src']))
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
    global bilder
    global dirPath
    date = request.json
    try:
        received_year = date['year']
        received_month = date['month']
        received_day = date['day']
        dirPath = f'static/Bilder/{received_year}/{received_month}/{received_day}/'
        bilder = folderstructure.images(dirPath)
        response.body = json.dumps({'bilder':bilder})
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
                                'exposoure':exif_data['ExposureTime'],
                                'fnum':exif_data['FNumber'],
                                'iso':exif_data['ISOSpeedRatings'],
                                'focal_length':exif_data['FocalLength']
                                })
    return response

@route('/api/bin', method = 'POST')
def delete():
    picture = request.json
    folderstructure.delete_picture(picture['src'])

if __name__ == '__main__':
    bilder = []
    folderstructure.sort('static/Bilder/')
    sort_tags('static/Bilder/')
    folderstructure.delete_image_backup('static/Bilder/')
    run(debug=True, reloader=True)