from background_task.models import Task
from background_task.models import CompletedTask

from background_task import background
from app_content.models import Lecture

from .utils import get_jwt_token, get_upload_link, get_full_video_info, get_drm_info_from_video_info, upload_to_cdn
from .utils import PROCESSING_NOT_STARTED, PROCESSING_READY_TO_START, PROCESSING_IN_PROGRESS, PROCESSING_FINISHED

import os
import time

from logging import getLogger

logger = getLogger(__name__)

@background(schedule=1)
def process_videos():
    non_processed_videos = Lecture.objects.filter(processing_state=PROCESSING_READY_TO_START)
    for entry in non_processed_videos:
        if not os.path.exists(entry.video_file.path):
            logger.error('Failed to upload video {}: file does not exist'.format(entry.video_file.path))
            continue

        jwt_token = get_jwt_token()
        if jwt_token == None:
            logger.error('Can not upload {}: failed to get JWT token'.format(entry.video_file.path))
            continue

        upload_link = get_upload_link()
        if upload_link == None:
            logger.error('Can not upload {}: failed to get upload link'.format(entry.video_file.path))
            continue

        video_uuid = upload_to_cdn(upload_link, jwt_token, entry.video_file.path)
        if None == video_uuid:
            logger.error('Failed to upload {}: upstream returned error.'.format(entry.video_file.path))
            continue

        entry.video_uuid = video_uuid
        entry.processing_state = PROCESSING_IN_PROGRESS
        entry.save()

@background(schedule=1)
def finalize_videos():
    non_finalized_videos = Lecture.objects.filter(processing_state=PROCESSING_IN_PROGRESS)
    for entry in non_finalized_videos:
        full_video_info = get_full_video_info(entry.video_uuid)
        if full_video_info == None:
            logger.error('Failed to get info for video {} (uuid {})'.format(entry.video_file.path, entry.video_uuid))
            continue

        drm_info = get_drm_info_from_video_info(full_video_info)
        if drm_info == None:
            continue

        if 'dash' in drm_info:
            entry.dash_url = drm_info['dash']

        if 'hls' in drm_info:
            entry.hls_url = drm_info['hls']

        if 'widevine' in drm_info:
            entry.widevine_url = drm_info['widevine']

        if 'playready' in drm_info:
            entry.playready_url = drm_info['playready']

        if 'fairplay' in drm_info:
            if 'server' in drm_info['fairplay']:
                entry.fairplay_url = drm_info['fairplay']['server']
            if 'certificate' in drm_info['fairplay']:
                entry.fairplay_certificate_url = drm_info['fairplay']['certificate']

        entry.processing_state = PROCESSING_FINISHED
        entry.save()

Task.objects.all().delete()
CompletedTask.objects.all().delete()

process_videos(repeat=30)
finalize_videos(repeat=30)
