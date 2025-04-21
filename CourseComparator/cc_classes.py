from typing import List, Optional


class Course:
    """
    课程类

    表示一门课程的基本信息，包括课程代码、课程名称、学分和是否必修
    """

    def __init__(
        self, course_code: str, course_name: str, credit: float, required: bool
    ):
        """
        初始化课程对象

        Args:
            course_code: 课程代码
            course_name: 课程名称
            credit: 课程学分
            required: 是否为必修课
        """
        self.course_code = course_code
        self.course_name = course_name
        self.credit = credit
        self.required = required

    def __repr__(self) -> str:
        """
        返回课程对象的字符串表示，用于调试

        Returns:
            str: 课程对象的字典表示
        """
        return str(
            {
                "course_code": self.course_code,
                "course_name": self.course_name,
                "credit": self.credit,
                "required": self.required,
            }
        )

    def __str__(self) -> str:
        """
        返回课程对象的字符串表示，用于显示

        Returns:
            str: 格式化的课程信息字符串
        """
        return f"{self.course_code}\t{self.course_name}\t{self.credit} 学分\t{'必修' if self.required else '选修'}"

    def __eq__(self, other: "Course") -> bool:
        """
        判断两个课程是否相等

        Args:
            other: 另一个课程

        Returns:
            bool: 如果两个课程的所有属性都相同，则返回True，否则返回False
        """
        if not isinstance(other, Course):
            return False
        return (
            self.course_code == other.course_code
            and self.course_name == other.course_name
            and self.credit == other.credit
            and self.required == other.required
        )

    def __gt__(self, other: "Course") -> bool:
        """
        判断当前课程是否可以完全涵盖另一个不同的课程(即虽不同但也可冲抵的情况)

        1. 两个课程不完全相同
        2. 课程代码相同
        3. 课程名称相同
        4. 当前课程(旧的)学分大于等于另一个课程(新的)
        5. 如果当前课程(旧的)是选修，另一个课程(新的)不能是必修

        Args:
            other: 另一个课程

        Returns:
            bool: 如果当前课程可以完全涵盖另一个不同的课程，则返回True，否则返回False
        """
        if not isinstance(other, Course):
            return False
        # 不能完全一致
        if self == other:
            return False
        # 课程代码必须相同
        if self.course_code != other.course_code:
            return False
        # 课程名必须相同
        if self.course_name != other.course_name:
            return False
        # 当前课程学分必须大于等于另一个课程
        if self.credit > other.credit:
            return False
        # 选修不能转必修
        if not self.required and other.required:
            return False
        return True


class CoursePair:
    """
    课程对类

    表示新旧两门课程的对比，用于显示课程变化
    """

    def __init__(self, old_course: Course, new_course: Course):
        """
        初始化课程对对象

        Args:
            old_course: 旧课程
            new_course: 新课程
        """
        self.old_course = old_course
        self.new_course = new_course

    def __repr__(self) -> str:
        """
        返回课程对对象的字符串表示，用于调试

        Returns:
            str: 课程对对象的字典表示
        """
        return str(
            {
                "old": {
                    "course_code": self.old_course.course_code,
                    "course_name": self.old_course.course_name,
                    "credit": self.old_course.credit,
                    "required": self.old_course.required,
                },
                "new": {
                    "course_code": self.new_course.course_code,
                    "course_name": self.new_course.course_name,
                    "credit": self.new_course.credit,
                    "required": self.new_course.required,
                },
            }
        )

    def __str__(self) -> str:
        """
        返回课程对对象的字符串表示，用于显示

        显示新旧课程的对比，包括课程代码、课程名称、学分和是否必修
        如果某项属性发生变化，会添加标记：
        - [ ! ]: 表示课程代码或课程名称变化
        - [ + ]: 表示学分增加或从选修变为必修
        - [ - ]: 表示学分减少或从必修变为选修

        Returns:
            str: 格式化的课程对比字符串
        """
        # 准备标记
        code_mark = (
            " [ ! ]"
            if self.old_course.course_code != self.new_course.course_code
            else ""
        )
        name_mark = (
            " [ ! ]"
            if self.old_course.course_name != self.new_course.course_name
            else ""
        )

        # 学分标记
        credit_mark = ""
        if self.old_course.credit != self.new_course.credit:
            credit_mark = (
                " [ + ]"
                if self.new_course.credit > self.old_course.credit
                else " [ - ]"
            )

        # 选必修标记
        required_mark = ""
        if self.old_course.required != self.new_course.required:
            required_mark = " [ + ]" if self.new_course.required else " [ - ]"

        # 计算各项最大宽度
        max_code_width = max(
            len(self.old_course.course_code),
            len(self.new_course.course_code) + len(code_mark),
        )
        max_name_width = max(
            len(self.old_course.course_name),
            len(self.new_course.course_name) + len(name_mark),
        )
        max_credit_width = max(
            len(f"{self.old_course.credit} 学分"),
            len(f"{self.new_course.credit} 学分") + len(credit_mark),
        )
        max_required_width = max(len("必修"), len("选修") + len(required_mark))

        # 构建格式化字符串
        format_str = f"{{prefix}}  {{code:<{max_code_width}}}\t{{name:<{max_name_width}}}\t{{credit:<{max_credit_width}}}\t{{required:<{max_required_width}}}"

        # 构建两行输出
        old_line = format_str.format(
            prefix="OLD:",
            code=self.old_course.course_code,
            name=self.old_course.course_name,
            credit=f"{self.old_course.credit} 学分",
            required="必修" if self.old_course.required else "选修",
        )

        new_line = format_str.format(
            prefix="NEW:",
            code=f"{self.new_course.course_code}{code_mark}",
            name=f"{self.new_course.course_name}{name_mark}",
            credit=f"{self.new_course.credit} 学分{credit_mark}",
            required=f"{'必修' if self.new_course.required else '选修'}{required_mark}",
        )

        return f"{old_line}\n{new_line}"


class CourseSet:
    """
    课程集合类

    表示一组课程，提供课程集合的操作方法
    """

    def __init__(self, courses: Optional[List[Course]] = None):
        """
        初始化课程集合对象

        Args:
            courses: 课程列表，默认为None（空列表）
        """
        self.courses = courses or []
        self._validate_courses()

    def _validate_courses(self) -> None:
        """
        验证课程集合中是否有重复的课程代码或课程名

        Raises:
            ValueError: 如果存在重复的课程代码或课程名
        """
        code_set = set()
        name_set = set()
        for course in self.courses:
            if course.course_code in code_set:
                raise ValueError(f"课程代码重复: {course.course_code}")
            if course.course_name in name_set:
                raise ValueError(f"课程名重复: {course.course_name}")
            code_set.add(course.course_code)
            name_set.add(course.course_name)

    def append(self, course: Course) -> None:
        """
        添加单个课程到集合中

        Args:
            course: 要添加的课程

        Raises:
            ValueError: 如果课程代码或课程名已存在
        """
        if any(c.course_code == course.course_code for c in self.courses):
            raise ValueError(f"课程代码重复: {course.course_code}")
        if any(c.course_name == course.course_name for c in self.courses):
            raise ValueError(f"课程名重复: {course.course_name}")
        self.courses.append(course)

    def __add__(self, other: "CourseSet") -> "CourseSet":
        """
        合并两个课程集合, 用于聚合同一方案的不同学期

        Args:
            other: 另一个课程集合

        Returns:
            CourseSet: 合并后的新课程集合

        Raises:
            TypeError: 如果other不是CourseSet类型
        """
        if not isinstance(other, CourseSet):
            raise TypeError("只能与 CourseSet 类型相加")
        new_courses = self.courses + other.courses
        return CourseSet(new_courses)

    def __sub__(self, other: "CourseSet") -> "CourseSetDelta":
        """
        用旧的培养方案减去新的培养方案, 用于计算两者之间的差异

        Args:
            other: 另一个课程集合

        Returns:
            CourseSetDelta: 表示两个课程集合差异的对象

        Raises:
            TypeError: 如果other不是CourseSet类型
        """
        if not isinstance(other, CourseSet):
            raise TypeError("只能与 CourseSet 类型相减")
        return CourseSetDelta(self, other)

    def __str__(self) -> str:
        """
        返回课程集合的字符串表示

        Returns:
            str: 所有课程的字符串表示，每行一个课程
        """
        return "\n".join(str(course) for course in self.courses)


class CourseSetDelta:
    """
    课程集合差异类

    表示两个课程集合之间的差异，包括可冲抵、待确认、需补修和需放弃的课程
    """

    def __init__(self, old_set: CourseSet, new_set: CourseSet):
        """
        初始化课程集合差异对象

        Args:
            old_set: 旧课程集合
            new_set: 新课程集合
        """
        self.consistent_or_including = []  # 可冲抵
        self.similar = []  # 待确认
        self.new_only = []  # 需补修
        self.old_only = []  # 需放弃

        self._calculate_delta(old_set, new_set)

    def _calculate_delta(self, old_set: CourseSet, new_set: CourseSet) -> None:
        """
        计算两个课程集合之间的差异

        Args:
            old_set: 旧课程集合
            new_set: 新课程集合
        """
        # 处理可冲抵和待确认的课程
        for old_course in old_set.courses:
            found = False
            for new_course in new_set.courses:
                # 1. 完全相等或可冲抵的情况
                if old_course == new_course or old_course > new_course:
                    self.consistent_or_including.append(
                        CoursePair(old_course, new_course)
                    )
                    found = True
                    break
                # 2. 课程代码相同或课程名称相同
                elif (
                    old_course.course_code == new_course.course_code
                    or old_course.course_name == new_course.course_name
                ):
                    self.similar.append(CoursePair(old_course, new_course))
                    found = True
                    break
            # 3. 未找到匹配的旧课程
            if not found:
                self.old_only.append(old_course)

        # 4. 处理需补修的课程
        for new_course in new_set.courses:
            if not any(
                old_course == new_course
                or old_course > new_course
                or old_course.course_code == new_course.course_code
                or old_course.course_name == new_course.course_name
                for old_course in old_set.courses
            ):
                self.new_only.append(new_course)

    def __str__(self) -> str:
        """
        返回课程集合差异的字符串表示

        Returns:
            str: 格式化的课程差异字符串，包括可冲抵、待确认、需补修和需放弃的课程
        """
        result = []

        if self.consistent_or_including:
            result.append("\n【可冲抵】\n")
            result.extend(str(pair) + "\n" for pair in self.consistent_or_including)

        if self.similar:
            result.append("\n【待确认】\n")
            result.extend(str(pair) + "\n" for pair in self.similar)

        if self.new_only:
            result.append("\n【需补修】\n")
            result.extend(str(course) + "\n" for course in self.new_only)

        if self.old_only:
            result.append("\n【需放弃】\n")
            result.extend(str(course) + "\n" for course in self.old_only)

        return "\n".join(result)
