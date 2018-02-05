import boto3, os, sys

FROM_BUCKET = 'ebiz-public-upload'
TO_BUCKET = 'ebiz17-team14-video-input-bucket'
DIR = 'dir/'
COUNT = 4

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

os.chdir(sys.path[0] + '/imgs/' + DIR)

count = 0
download_response = s3_client.list_objects_v2(Bucket=FROM_BUCKET, MaxKeys=COUNT)
for Content in download_response['Contents']:
  copy_source = {'Bucket': FROM_BUCKET, 'Key': Content['Key']}
  s3_resource.meta.client.copy(copy_source, TO_BUCKET, Content['Key'])
  #download
  #s3_resource.Bucket(FROM_BUCKET).download_file(Content['Key'], Content['Key'])

""" upload
imgs = os.listdir('.')
for img in imgs:
  if count == COUNT:
  	break
  if img.split('.')[1] in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'raw']:
    s3_resource.meta.client.upload_file(img, TO_BUCKET, img)
    count += 1
    print count, img, ' uploaded !'
"""
<<<<<<< HEAD
=======
imgs = os.listdir('.')
for img in imgs:
  if count == COUNT:
  	break
  if img.split('.')[1] in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif', 'raw']:
    with open(img, 'rb') as data:
        s3_client.upload_fileobj(data, TO_BUCKET, img)
        count += 1
        print count, img, ' uploaded !'
>>>>>>> 766cbf6ff21c81cd755b3540c871ea0f007e4b46
