import logging
import random
import string
import aiobotocore
from PIL import Image
from configuration import S3

BUCKET = S3.get('bucket')
REGION = S3.get('region')
AWS_SECRET_KEY = S3.get('secret_access_key')
AWS_KEY_ID = S3.get('accesskeyid')
BASE_STRING = string.ascii_letters + string.digits


async def s3_image_upload(dataset_id: int, data) -> dict:
    filename = data['file'].filename
    file = data['file'].file
    image = Image.open(file)
    width, height = image.size
    s3_filename = ''.join([random.choice(BASE_STRING) for _ in range(32)])
    key = f"{dataset_id}/{s3_filename}"

    logging.info(f'File ({filename}) for uploading to dataset: {dataset_id}')
    aws_session = aiobotocore.get_session()
    async with aws_session.create_client(service_name='s3',
                                         region_name=REGION,
                                         aws_secret_access_key=AWS_SECRET_KEY,
                                         aws_access_key_id=AWS_KEY_ID,
                                         verify=False) as client:
        file.seek(0)
        await client.put_object(Body=file,
                                Bucket=BUCKET,
                                Key=key,
                                ACL='public-read'
                                )
    ret = dict(image_name=filename,
               image_link=f"https://s3-{REGION}.amazonaws.com/{BUCKET}/{key}",
               width=width,
               height=height,
               dataset_id=dataset_id
               )
    return ret
