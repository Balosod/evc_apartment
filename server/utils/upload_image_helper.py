import base64
import uuid
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS


async def upload_image_to_file_path(images, model_name):
    image_obj_list = []
    for image in images:
        img_name = str(uuid.uuid4())[:10] + ".png"
        image_as_bytes = str.encode(image)
        img_recovered = base64.b64decode(image_as_bytes)

        with open("server/media/image/uploaded_" + img_name, "wb") as f:
            f.write(img_recovered)

        upload_image = model_name(
            img=f"http://localhost:8000/media/image/uploaded_{img_name}"
        )
        image_obj_list.append(upload_image)
        await upload_image.create()
    return image_obj_list


async def upload_image_to_S3_bucket(images, model_name):
    image_obj_list = []
    for image in images:
        img_name = str(uuid.uuid4())[:10] + ".png"
        image_as_bytes = str.encode(image)
        img_recovered = base64.b64decode(image_as_bytes)

        client.put_object(
            Bucket=CONFIG_SETTINGS.BUCKET,
            Body=img_recovered,
            Key=f"image/{img_name}",
            ACL=CONFIG_SETTINGS.ACL,
            ContentType="image/png",
        )

        upload_image = model_name(
            img=f"https://postatusapistorage.nyc3.digitaloceanspaces.com/image/{img_name}"
        )
        image_obj_list.append(upload_image)
        await upload_image.create()
    return image_obj_list
