"""test"""
import os

from icourse163.CourseCatalog import CourseCatalog
from icourse163.detail import get_detail


here = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    course_url = input("course url: ")
    course = CourseCatalog(course_url)
    if not os.path.exists("output"):
        os.mkdir("output")

    # 创建课程目录
    course_path = os.path.join(here, "output", course.courseName)
    print(course_path)
    if not os.path.exists(course_path):
        os.mkdir(course_path)

    # 创建章节目录
    for chapter in course.chapters:
        print(chapter["chapterName"])
        chapter_path = os.path.join(course_path, chapter["chapterName"])
        print(chapter_path)
        if not os.path.exists(chapter_path):
            os.mkdir(chapter_path)

    # 创建课时目录
    for lesson in course.lessons:
        lesson_path = os.path.join(course_path, lesson["chapterName"], lesson["lessonName"])
        print(lesson_path)
        if not os.path.exists(lesson_path):
            os.mkdir(lesson_path)

    # 下载
    for video in course.videos:
        # print(course.videos)
        detail = get_detail(video)
        if not detail:
            continue
        videoName = detail["videoName"]
        file_url = detail["file_url"]
        file_path = os.path.join(course_path, video["chapterName"], video["lessonName"], video["videoName"] + ".mp4")
        with open(file_path, "w") as f:
            f.write(file_url)
            print(f"\n{videoName}下载完成\n路径：{file_path}")

    for pdf in course.pdfs:
        detail = get_detail(pdf)
        if not detail:
            continue
        pdfName = detail["pdfName"]
        file_url = detail["file_url"]
        file_path = os.path.join(course_path, pdf["chapterName"], pdf["lessonName"], pdf["pdfName"] + ".pdf")
        with open(file_path, "w") as f:
            f.write(file_url)
            print(f"\n{pdfName}下载完成\n路径：{file_path}")
