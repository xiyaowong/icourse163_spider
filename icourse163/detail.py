"""
资源详情
"""
import re

import requests

_headers = {
    "user-agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/80.0.3987.149 Safari/537.36")
}
_detail_url = "https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr"
_detail_data = {
    'callCount': '1',
    'scriptSessionId': '${scriptSessionId}190',
    'httpSessionId': '184f53a7e78148749e219d745b52e6a7',
    'c0-scriptName': 'CourseBean',
    'c0-methodName': 'getLessonUnitLearnVo',
    'c0-id': '0',
    'c0-param0': None,  # number:{contentId}
    'c0-param1': None,  # number:{contentType}
    'c0-param2': 'number:0',
    'c0-param3': None,  # number:{videoId/pdfId}
    'batchId': '1584867320893',
}


def get_detail(source: dict) -> dict:
    """
    Inputs:
        source长这样
        {
            chapterId:
            chapterName:
            lessonId:
            lessongName:
            contentId:
            contentTye:
            videoId/pdfId:
            videoName/pdfName:
        }
    Returns:
        在source的基础上增加一个下载地址file_url
    """
    if source["contentType"] == "1":
        return _get_video_detail(source)
    return _get_pdf_detail(source)


def _get_video_detail(source) -> dict:
    _detail_data["c0-param0"] = source["contentId"]
    _detail_data["c0-param1"] = source["contentType"]
    _detail_data["c0-param3"] = source["videoId"]
    rep = requests.post(_detail_url, data=_detail_data, timeout=10)
    re_videoUrl = r'mp4\w+Url="(.*?)"'
    urls = re.findall(re_videoUrl, rep.text)
    for quantity in ["shd.mp4", "hd.mp4", "sd.mp4"]:
        for url in urls:
            if quantity in url:
                return {
                    **source,
                    "file_url": url,
                }
    return None


def _get_pdf_detail(source) -> dict:
    _detail_data["c0-param0"] = source["contentId"]
    _detail_data["c0-param1"] = source["contentType"]
    _detail_data["c0-param3"] = source["pdfId"]
    re_pdfUrl = r'textOrigUrl:"(.*?)"'
    rep = requests.post(_detail_url, data=_detail_data, timeout=10)
    urls = re.findall(re_pdfUrl, rep.text)
    return {
        **source,
        "file_url": urls[0],
    }
