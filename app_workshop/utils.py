from io import BytesIO
from io import StringIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.conf import settings
import os.path

from logging import getLogger

import json
import requests
import traceback

PROCESSING_NOT_STARTED = 0
PROCESSING_READY_TO_START = 1
PROCESSING_IN_PROGRESS = 2
PROCESSING_FINISHED = 3

logger = getLogger(__name__)

def fetch_pdf_resources(uri, rel):
    import os.path
    from django.conf import settings
    path = os.path.join(settings.STATIC_ROOT,
                        uri.replace(settings.STATIC_URL, ""))
    # path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ''))
    # print(path)
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode(
    #     'UTF-8')), result, encoding='utf-8', link_callback=fetch_pdf_resources)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

#
# CDN API utils
#

def get_jwt_token():
    try:
        r = requests.get(settings.CDN_JWT_URL,
                         timeout=settings.CDN_TIMEOUT_SECONDS,
                         headers={"X-AUTH-TOKEN": settings.CDN_API_TOKEN})

        if r.status_code != 200:
            return None
    except:
        logger.error('Failed to get JWT token from {}: {}'.format(settings.CDN_JWT_URL, traceback.format_exc()))
        return None

    result = None
    try:
        json_response = json.loads(r.text) # response is supposed to be "somestring" (with quotes!), which is a valid JSON
        result = json_response
    except:
        result = None

    return result

def get_upload_link():
    try:
        r = requests.get(settings.CDN_RECEIVE_UPLOAD_LINK_URL,
                         **settings.CDN_REQUESTS_COMMON_PARAMS)

        if r.status_code != 200:
            return None
    except:
        logger.error('Failed to get upload link from {}: {}'.format(settings.CDN_RECEIVE_UPLOAD_LINK_URL, traceback.format_exc()))
        return None

    result = None
    try:
        json_response = json.loads(r.text)
        result = json_response['upload_link']
    except:
        result = None

    return result

def get_full_video_info(video_uuid):
    try:
        r = requests.get(settings.CDN_VIDEO_INFO_URL.format(video_uuid),
                         **settings.CDN_REQUESTS_COMMON_PARAMS)

        if r.status_code != 200:
            return None
    except:
        logger.error('Failed to get full video info from {}: {}'.format(settings.CDN_VIDEO_INFO_URL.format(video_uuid), traceback.format_exc()))
        return None

    result = None
    try:
        result = json.loads(r.text)
    except:
        result = None

    return result

def get_drm_info_from_video_info(video_info):
    result = None
    if 'results' not in video_info:
        return result

    for result_entry in video_info['results']:
        if 'profile' not in result_entry:
            continue

        if 'name' not in result_entry['profile']:
            continue

        if result_entry['profile']['name'] != 'Transcode & DRM':
            continue

        if 'result' not in result_entry:
            continue

        result = result_entry['result']

    return result

def upload_to_cdn(upload_link, jwt_token, video_file):
    request_params = dict(settings.CDN_REQUESTS_COMMON_PARAMS)
    request_params['headers'].update({'JWT': jwt_token})
    request_params.update({'files': {os.path.basename(video_file): open(video_file, 'rb')}})
    request_params.update({'timeout': settings.CDN_FILE_UPLOAD_TIMEOUT_SECONDS})
    request_params.update({'params': {'add': 1, 'run': 1}})

    try:
        r = requests.post(upload_link, **request_params)
        if r.status_code != 200:
            return None
    except:
        global logger
        logger.error('Failed to upload video to {}: {}'.format(upload_link, traceback.format_exc()))
        return None

    response_json = None
    try:
        response_json = json.loads(r.text)
    except:
        response_json = None

    if response_json == None:
        return None

    fileName = os.path.basename(video_file)

    if fileName not in response_json:
        return None

    if len(response_json[fileName]) == 0:
        return None

    file_name_entry = None
    try:
        file_name_entry = response_json[fileName].pop()
    except:
        global logger
        logger.error('Failed to read uploaded video info from {}: {}'.format(upload_link, traceback.format_exc()))
        return None
        
    if 'video_uuid' not in file_name_entry:
        return None

    return file_name_entry['video_uuid']
