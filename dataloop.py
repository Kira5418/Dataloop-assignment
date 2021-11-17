import requests
import flickrapi
from datetime import timezone
import datetime
from typing import ItemsView
import dtlpy as dl
from dtlpy.entities import item
from dtlpy.repositories import items

if dl.token_expired():
    dl.login()

project = dl.projects.get(project_id='a17ae4f0-c7f1-490c-91cb-624d17f0ff1d')
# print(project)
dataset = project.datasets.get(dataset_id='618961d38474aed1dd43afe8')
# dataset.print()
#a
# dataset.add_label(label_name='auto')
labels = dataset.labels
#b
item = dataset.items.get(filepath='/IMG_1046.JPG')
builder = item.annotations.builder()
# builder.add(annotation_definition = dl.Classification(label='auto2'))
# item.annotations.upload(builder)
#c
# builder.add(annotation_definition = dl.Classification(label='model_version 1'))
# item.annotations.upload(builder)
# model_version = int(item.annotations.get(annotation_id='61941b4e1e7e1d4377b94bc5').split('model_version ')[1])
# model_version += 1
#e
# to_upload = list()
# dataset.items.upload(local_path=[
#                      r'C:/Users/Kira/Pictures/Traveling/Madrid_Barcelona 2012/IMG_1003.JPG'])

# item = dataset.items.get(item_id='618962061e07e17258c0a4d1')

# dt = datetime.datetime.now(timezone.utc)
#
# utc_time = dt.replace(tzinfo=timezone.utc)
# utc_timestamp = utc_time.timestamp()
#
# item.metadata['collected'] = utc_timestamp
# item = item.update()


#f
api_key = u'7a2be53e7aa745760dc92ca2e0434ae2'
api_secret = u'8e58032c1090dcdc'


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
photos = flickr.photos.search(api_key=api_key, user_id='194378719@N05', tags='cat, dogs', per_page='5')
# sets = flickr.photosets.getList(user_id='73509078@N00')
# title = sets['photosets'
# ]['photoset'][0]['title']['_content']
print('First set title: %s' % photos)
# print('type: %s', type(photos))
folder='Flickr'
try:
    dataset = project.datasets.get(dataset_name=folder)
except :
    dataset = project.datasets.create(dataset_name=folder)

# url_list = []

for photo in photos['photos']['photo']:
    id = photo["id"]
    server = photo["server"]
    secret = photo["secret"]
    name = id + "_" + secret + "_n"
    url_path = "https://live.staticflickr.com/" + server + "/" + name + ".jpg"
    # info = flickr.photos.getInfo(api_key=api_key, photo_id=id)
    # # print(info['photo']['urls']['url'][0]['_content'])
    # url_path = info['photo']['urls']['url'][0]['_content']
    print(url_path+'\n')
    # url_list.append(info['photo']['urls']['url'][0]['_content'])
    link = dl.UrlLink(ref=url_path, mimetype='image', name=name+'.jpg')
    # Upload link
    # dataset.items.upload(local_path=link)
    #g
    # string = "cat bike dog"
    # for ll in string.split(" "):
    #     item1 = dataset.items.get(filepath='/' + name + '.jpg_link.json')
    #     builder1 = item1.annotations.builder()
    #     builder1.add(annotation_definition = dl.Classification(label=ll))
    #     item1.annotations.upload(builder1)
    #i
filters = dl.Filters()
filters.resource = dl.FiltersResource.ANNOTATION # filters with and

filters.add(field='label', values='bike', method=dl.FiltersMethod.AND)# optional - return results sorted by ascending creation date
filters.sort_by(field=dl.FILTERS_KNOWN_FIELDS_CREATED_AT)
# Get filtered annotations list
pages = dataset.annotations.list(filters=filters)
# Iterate through the annotations - Go over all annotations and print the properties
for page in pages:
        for annotation in page:
                annotation.print()
# annotation = item.annotations.get(annotation_id='your-annotation-id-number')
# print(annotation)
# print(dataset.items.get(item_id = 'my_item_Id'))


#g for list
# print(url_list)
# Create link list
# links = dl.UrlLink.from_list(url_list=url_list)
# Upload links
# dataset.items.upload(local_path=links)