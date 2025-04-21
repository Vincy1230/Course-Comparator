from typing import Callable
from .cc_classes import Course, CourseSet
import csv
import pickle
from pathlib import Path


# 全局唯一的0学期对象，表示刚入学的状态
EMPTY_SEMESTER = CourseSet()


def init(data_dir: str) -> Callable[[str, str, int], CourseSet]:
    """
    创建课程数据加载器

    Args:
        data_dir: 数据目录的路径

    Returns:
        Callable[[str, str, int], CourseSet]: 加载器函数，接受专业名称、年份和学期作为参数，返回课程集合
    """
    # 确保数据目录存在
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"数据目录不存在: {data_dir}")

    # 创建缓存目录
    cache_dir = data_path / "__cc_cache__"
    cache_dir.mkdir(exist_ok=True)

    def loader(major: str, year: str, semester: int) -> CourseSet:
        """
        加载指定专业、年份和学期的课程数据

        Args:
            major: 专业名称
            year: 年份
            semester: 学期数（0-8，0表示刚入学的状态）

        Returns:
            CourseSet: 指定学期的课程集合

        Raises:
            FileNotFoundError: 如果专业目录不存在
            ValueError: 如果学期数不在有效范围内
        """
        # 处理 0 学期（刚入学的状态）
        if semester == 0:
            return EMPTY_SEMESTER

        # 验证学期数
        if semester < 0 or semester > 8:
            raise ValueError(f"学期数必须在0-8之间，当前值: {semester}")

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

            # 如果数据文件没有更新，直接使用缓存
            if not data_files_updated:
                with open(cache_file, "rb") as f:
                    course_sets = pickle.load(f)

                    # 如果学期数大于可用的学期数，返回最后一个学期的课程集合
                    if semester > len(course_sets):
                        return course_sets[-1]

                    # 计算前semester个学期的课程集合之和
                    result = CourseSet()
                    for i in range(semester):
                        result = result + course_sets[i]

                    return result

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

        # 如果学期数大于可用的学期数，返回最后一个学期的课程集合
        if semester > len(course_sets):
            return course_sets[-1]

        # 计算前semester个学期的课程集合之和
        result = CourseSet()
        for i in range(semester):
            result = result + course_sets[i]

        return result

    return loader
