import base64
import uuid
from ..utils.s3_storage import client
from ..settings import CONFIG_SETTINGS


async def upload_video_to_file_path(videos, model_name):
    video_obj_list = []
    for video in videos:
        video_name = str(uuid.uuid4())[:10] + ".mp4"
        video_as_bytes = str.encode(video)
        video_recovered = base64.b64decode(video_as_bytes)

        with open("server/media/video/uploaded_" + video_name, "wb") as f:
            f.write(video_recovered)

        upload_video = model_name(
            img=f"http://localhost:8000/media/video/uploaded_{video_name}"
        )
        video_obj_list.append(upload_video)
        await upload_video.create()
    return video_obj_list


async def upload_video_to_S3_bucket(videos, model_name):
    video_obj_list = []
    for video in videos:
        video_name = str(uuid.uuid4())[:10] + ".mp4"
        video_as_bytes = str.encode(video)
        video_recovered = base64.b64decode(video_as_bytes)

        client.put_object(
            Bucket=CONFIG_SETTINGS.BUCKET,
            Body=video_recovered,
            Key=f"video/{video_name}",
            ACL=CONFIG_SETTINGS.ACL,
            ContentType="video/mp4",
        )

        upload_video = model_name(
            img=f"https://postatusapistorage.nyc3.digitaloceanspaces.com/video/{video_name}"
        )
        video_obj_list.append(upload_video)
        await upload_video.create()
    return video_obj_list
