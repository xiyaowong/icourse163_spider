# icourse63_spider
爱课程(中国大学mooc)爬虫

## 简单使用
```py
In [1]: from icourse63 import CourseCatalog

In [2]: url = "https://www.icourse63.org/course/NEU-1002525010"

In [3]: course = CourseCatalog(url)  # 或者：course = CourseCatalog();course.get(url)

In [4]: course.courseName  # 课程名
Out[4]: '心理学入门'

In [5]: course.chapters  # 课程章节
Out[5]:
[{'chapterId': '1214824482', 'chapterName': '第一周 绪论'},
  ...]

In [6]: course.lessons  # 课程课时
Out[6]:
[{'chapterId': '1214824482',
  'chapterName': '第一周 绪论',
  'lessonId': '1223273737',
  'lessonName': '1.1 心理学的研究对象与任务'},
  ...]

In [7]: course.pdfs  # 课程教案相关
Out[7]:
[{'chapterId': '1214824482',
  'chapterName': '第一周 绪论',
  'lessonId': '1223273739',
  'lessonName': '1.3 现代心理学的研究取向',
  'contentId': '1007896015',
  'contentType': '3',
  'pdfId': '1235189481',
  'pdfName': '第一周 绪论讲稿'},
  ...]

In [8]: course.videos  # 课程视频
Out[8]:
[{'chapterId': '1214824482',
  'chapterName': '第一周 绪论',
  'lessonId': '1223273737',
  'lessonName': '1.1 心理学的研究对象与任务',
  'contentId': '1010354353',
  'contentType': '1',
  'videoId': '1235189478',
  'videoName': '1.1 心理学的研究对象与任务'},
  ...]

```
### 还是看源码注释和`example.py`吧，挺简单的
