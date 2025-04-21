from typing import Literal, List, Callable
from .cc_classes import Course, CourseSimilarity, CourseSet
import re
import os
import csv
import pickle
import time
from pathlib import Path


# 全局唯一的0学期对象，表示刚入学的状态
EMPTY_SEMESTER = CourseSet()


def similarity(course1: Course, course2: Course) -> CourseSimilarity:
    """
    计算两个课程的相似度

    Args:
        course1: 第一个课程
        course2: 第二个课程

    Returns:
        CourseSimilarity.CONSISTENT: 完全一致
        CourseSimilarity.INCLUDING: 不一致但前者包含后者（单向）
        CourseSimilarity.SIMILAR: 不一致、不包含但课程名相同，或去掉括号内容后相同
        CourseSimilarity.UNRELATED: 完全不相关
    """
    # 完全一致的情况
    if course1 == course2:
        return CourseSimilarity.CONSISTENT

    # 检查包含关系
    if course1 > course2:
        return CourseSimilarity.INCLUDING

    # 检查课程名相似度
    def clean_course_name(name: str) -> str:
        # 移除中英文括号及其内容
        return re.sub(r"[（(][^）)]*[）)]", "", name).strip()

    # 原始课程名相同
    if course1.course_name == course2.course_name:
        return CourseSimilarity.SIMILAR

    # 清理后的课程名相同
    if clean_course_name(course1.course_name) == clean_course_name(course2.course_name):
        return CourseSimilarity.SIMILAR

    # 其他情况视为不相关
    return CourseSimilarity.UNRELATED


def init(data_dir: str) -> Callable[[str, str], List[CourseSet]]:
    """
    创建课程数据加载器

    Args:
        data_dir: 数据目录的路径

    Returns:
        加载器函数，接受专业名称和年份作为参数，返回课程集合列表
    """
    # 确保数据目录存在
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"数据目录不存在: {data_dir}")

    # 创建缓存目录
    cache_dir = data_path / "__cc_cache__"
    cache_dir.mkdir(exist_ok=True)

    def loder(major: str, year: str) -> List[CourseSet]:
        """
        加载指定专业和年份的课程数据

        Args:
            major: 专业名称
            year: 年份

        Returns:
            课程集合列表，包含8个学期的课程
        """
        # 构建数据目录路径
        major_dir = data_path / major / year
        if not major_dir.exists():
            raise FileNotFoundError(f"专业目录不存在: {major_dir}")

        # 构建缓存文件路径
        cache_file = cache_dir / f"{major}_{year}.pkl"

        # 检查缓存是否存在且是最新的
        if cache_file.exists():
            # 获取缓存文件的修改时间
            cache_mtime = cache_file.stat().st_mtime

            # 检查数据文件是否有更新
            data_files_updated = False
            for i in range(1, 9):
                csv_file = major_dir / f"{i}.csv"
                if csv_file.exists() and csv_file.stat().st_mtime > cache_mtime:
                    data_files_updated = True
                    break

            # 如果数据文件没有更新，直接返回缓存
            if not data_files_updated:
                with open(cache_file, "rb") as f:
                    return pickle.load(f)

        # 如果没有缓存或缓存已过期，重新加载数据
        course_sets = []
        for i in range(1, 9):
            csv_file = major_dir / f"{i}.csv"
            if not csv_file.exists():
                # 如果某个学期的文件不存在，添加一个空的课程集合
                course_sets.append(CourseSet())
                continue

            courses = []
            with open(csv_file, "r", encoding="GBK") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    course = Course(
                        course_code=row["course_code"],
                        course_name=row["course_name"],
                        credit=float(row["credit"]),
                        required=bool(int(row["required"])),
                    )
                    courses.append(course)

            course_sets.append(CourseSet(courses))

        # 保存缓存
        with open(cache_file, "wb") as f:
            pickle.dump(course_sets, f)

        return course_sets

    return loder


def query(
    loader: Callable[[str, str], List[CourseSet]], major: str, year: str, semester: int
) -> CourseSet:
    """
    查询特定学期的课程集合

    Args:
        loader: 课程数据加载器函数
        major: 专业名称
        year: 年份
        semester: 学期数（0-8，0表示刚入学的状态）

    Returns:
        指定学期的课程集合
    """
    # 处理0学期（刚入学的状态）
    if semester == 0:
        return EMPTY_SEMESTER

    # 验证学期数
    if semester < 0 or semester > 8:
        raise ValueError(f"学期数必须在0-8之间，当前值: {semester}")

    # 加载课程数据
    course_sets = loader(major, year)

    # 如果学期数大于可用的学期数，返回最后一个学期的课程集合
    if semester > len(course_sets):
        return course_sets[-1]

    # 计算前semester个学期的课程集合之和
    result = CourseSet()
    for i in range(semester):
        result = result + course_sets[i]

    return result
