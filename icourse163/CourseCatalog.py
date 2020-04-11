import re
from typing import List

import requests


class CourseCatalog:
    """
    获得课程有关信息
    """
    __headers = {
        "user-agent": ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/80.0.3987.149 Safari/537.36")
    }
    __list_url = "https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr"
    __list_data = {
        "callCount": "1",
        "scriptSessionId": "${scriptSessionId}190",
        "httpSessionId": "184f53a7e78148749edf19d745b52e6a7",
        "c0-scriptName": "CourseBean",
        "c0-methodName": "getMocTermDto",
        "c0-id": "0",
        "c0-param0": None,  # number:{termId}
        "c0-param1": "number:0",
        "c0-param2": "boolean:true",
        "batchId": "1584888320712",
    }

    def __init__(self, url=None):
        self.courseName: str = None
        self.chapters: List[dict] = None
        self.lessons: List[dict] = None
        self.videos: List[dict] = None
        self.pdfs: List[dict] = None
        if url is not None:
            self.get(url)

    def get(self, url):
        """
        循序不能改
        """
        termId = self.__get_termId(url)
        assert termId is not None
        text = self.__get_catalog_text(termId)
        assert text is not None
        self.__get_courseName(text)
        self.__get_chapters(text)
        self.__get_lessons(text)
        self.__get_videos(text)
        self.__get_pdfs(text)

    def __get_termId(self, url):
        """
        获得课程id
        """
        rep = requests.get(url, headers=self.__headers, timeout=10)
        if rep.status_code == 200:
            termId = re.findall(r"termId=(\d+)", rep.text)
            if not termId:
                termId = re.findall(r'termId : "(\d+)",', rep.text)
            if termId:
                return termId[0]
        return None

    def __get_catalog_text(self, termId):
        """
        获得课程目录接口返回的原始数据
        """
        self.__list_data["c0-param0"] = str(termId)
        rep = requests.post(self.__list_url, data=self.__list_data, headers=self.__headers, timeout=10)
        if rep.status_code == 200:
            return rep.text
        return None

    def __get_courseName(self, text) -> str:
        """
        获得课程名 set self.courseName
        """
        re_courseName = r'courseName:"(.*?)",'
        courseName = re.findall(re_courseName, text)
        self.courseName = courseName[0].encode('utf-8').decode("unicode_escape").replace("/", "|").replace("\\", "|")
        return courseName

    def __get_chapters(self, text) -> list:
        """
        获得章节信息 set self.chapters
        Returns:
            返回一个章节列表每个元素是字典，字典包含章节chapterId和章节名chapterName
            {
                chapterId:
                chapterName:
            }
        """
        chapters = re.findall(r'homeworks=\w+;.+?id=(\d+).+?name="((.|\n)+?)";', text)
        data = []
        for chapter in chapters:
            data.append({
                "chapterId": chapter[0],
                "chapterName": chapter[1].encode('utf-8').decode("unicode_escape").replace("/", "|").replace("\\", "|"),
            })
        self.chapters = data
        return data

    def __get_lessons(self, text) -> list:
        """
        返回每一章包含的课 set self.lessons
        Returns:
            返回一个课堂列表每个元素是字典
            {
                chapterId:
                chapterName:
                lessonId:
                lessonName:
            }
        """
        data = []
        for chapter in self.chapters:
            chapterId = chapter["chapterId"]
            re_lessons = r'chapterId=' + str(chapterId) + \
                r'.+?contentType=1.+?id=(\d+).+?isTestChecked=false.+?name="(.*?)".+?test'
            lessons = re.findall(re_lessons, text)
            for lesson in lessons:
                data.append({
                    **chapter,
                    "lessonId": lesson[0],
                    "lessonName": lesson[1].encode('utf-8').decode("unicode_escape").replace("/", "|").replace("\\", "|"),
                })
        self.lessons = data
        return data

    def __get_videos(self, text) -> list:
        """
        返回每一课包含的视频, set self.videos
        Returns:
            返回一个视频列表每个元素是字典
            {
                chapterId:
                chapterName:
                lessonId:
                lessonName:
                videoId:
                contentId:
                contentType:
                videoName:
            }
        """
        data = []
        for lesson in self.lessons:
            lessonId = lesson["lessonId"]
            re_videos = r'contentId=(\d+).+contentType=(1).+id=(\d+).+lessonId=' + str(lessonId) + r'.+name="(.+)"'
            videos = re.findall(re_videos, text)
            for video in videos:
                data.append({
                    **lesson,
                    "contentId": video[0],
                    "contentType": video[1],
                    "videoId": video[2],
                    "videoName": video[3].encode('utf-8').decode("unicode_escape").replace("/", "|").replace("\\", "|")
                })
        self.videos = data
        return data

    def __get_pdfs(self, text) -> list:
        """
        返回每一课包含的pdf即课件, set self.pdfs
        Returns:
            返回一个pdf列表每个元素是字典
            {
                chapterId:
                chapterName:
                lessonId:
                lessonName:
                pdfId:
                contentId:
                contentType:
                pdfName:
            }
        """
        data = []
        for lesson in self.lessons:
            lessonId = lesson["lessonId"]
            re_pdfs = r'contentId=(\d+).+contentType=(3).+id=(\d+).+lessonId=' + str(lessonId) + r'.+name="(.+)"'
            pdfs = re.findall(re_pdfs, text)
            for pdf in pdfs:
                data.append({
                    **lesson,
                    "contentId": pdf[0],
                    "contentType": pdf[1],
                    "pdfId": pdf[2],
                    "pdfName": pdf[3].encode('utf-8').decode("unicode_escape").replace("/", "|").replace("\\", "|"),
                })
        self.pdfs = data
        return data
