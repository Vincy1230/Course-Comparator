"""
课程比较器模块

该模块提供了课程比较和课程集合操作的功能，用于比较不同专业、不同年份的课程设置，
帮助用户了解课程变化，包括可冲抵、待确认、需补修和需放弃的课程。

主要组件：
- Course: 课程类，表示一门课程的基本信息
- CoursePair: 课程对类，表示两个课程之间的关系
- CourseSet: 课程集合类，表示一组课程
- CourseSetDelta: 课程集合差异类，表示两个课程集合之间的差异
- init: 创建课程数据加载器的函数
"""

from .cc_classes import (
    Course,
    CoursePair,
    CourseSet,
    CourseSetDelta,
)

from .cc_functions import init, init_internet, EMPTY_SEMESTER

__all__ = [
    "Course",
    "CoursePair",
    "CourseSet",
    "CourseSetDelta",
    "init",
    "init_internet",
    "EMPTY_SEMESTER",
]

__version__ = "0.1.0"
