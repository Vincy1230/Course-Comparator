from enum import Enum


class CourseSimilarity(Enum):
    CONSISTENT = "consistent"  # 完全一致
    INCLUDING = "including"  # 不一致但前者包含后者（单向）
    SIMILAR = "similar"  # 不一致、不包含但课程名相同，或去掉括号内容后相同
    UNRELATED = "unrelated"  # 完全不相关


class Course:
    def __init__(
        self, course_code: str, course_name: str, credit: float, required: bool
    ):
        self.course_code = course_code
        self.course_name = course_name
        self.credit = credit
        self.required = required

    def __repr__(self):
        return str(
            {
                "course_code": self.course_code,
                "course_name": self.course_name,
                "credit": self.credit,
                "required": self.required,
            }
        )

    def __str__(self):
        return f"{self.course_code}\t{self.course_name}\t{self.credit} 学分\t{'必修' if self.required else '选修'}"

    def __eq__(self, other):
        if not isinstance(other, Course):
            return False
        return (
            self.course_code == other.course_code
            and self.course_name == other.course_name
            and self.credit == other.credit
            and self.required == other.required
        )

    def __gt__(self, other):
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
        # 学分必须小于等于
        if self.credit < other.credit:
            return False
        # 必修不能转选修
        if self.required and not other.required:
            return False
        return True


class CoursePair:
    def __init__(self, old_course: Course, new_course: Course):
        self.old_course = old_course
        self.new_course = new_course

    def __repr__(self):
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

    def __str__(self):
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
    def __init__(self, courses: list[Course] | None = None):
        self.courses = courses or []
        self._validate_courses()

    def _validate_courses(self):
        """验证课程集合中是否有重复的课程代码或课程名"""
        code_set = set()
        name_set = set()
        for course in self.courses:
            if course.course_code in code_set:
                raise ValueError(f"课程代码重复: {course.course_code}")
            if course.course_name in name_set:
                raise ValueError(f"课程名重复: {course.course_name}")
            code_set.add(course.course_code)
            name_set.add(course.course_name)

    def append(self, course: Course):
        """添加单个课程"""
        if any(c.course_code == course.course_code for c in self.courses):
            raise ValueError(f"课程代码重复: {course.course_code}")
        if any(c.course_name == course.course_name for c in self.courses):
            raise ValueError(f"课程名重复: {course.course_name}")
        self.courses.append(course)

    def __add__(self, other):
        """合并两个课程集合"""
        if not isinstance(other, CourseSet):
            raise TypeError("只能与 CourseSet 类型相加")
        new_courses = self.courses + other.courses
        return CourseSet(new_courses)

    def __sub__(self, other):
        """计算两个课程集合的差异"""
        if not isinstance(other, CourseSet):
            raise TypeError("只能与 CourseSet 类型相减")
        return CourseSetDelta(self, other)

    def __str__(self):
        return "\n".join(str(course) for course in self.courses)


class CourseSetDelta:
    def __init__(self, old_set: CourseSet, new_set: CourseSet):
        self.consistent_or_including = []  # 可冲抵
        self.similar = []  # 待确认
        self.new_only = []  # 需补修
        self.old_only = []  # 需放弃

        self._calculate_delta(old_set, new_set)

    def _calculate_delta(self, old_set: CourseSet, new_set: CourseSet):
        """计算两个课程集合之间的差异"""
        # 处理可冲抵和待确认的课程
        for old_course in old_set.courses:
            found = False
            for new_course in new_set.courses:
                if old_course == new_course or old_course > new_course:
                    self.consistent_or_including.append(
                        CoursePair(old_course, new_course)
                    )
                    found = True
                    break
                elif (
                    old_course.course_code == new_course.course_code
                    or old_course.course_name == new_course.course_name
                ):
                    self.similar.append(CoursePair(old_course, new_course))
                    found = True
                    break
            if not found:
                self.old_only.append(old_course)

        # 处理需补修的课程
        for new_course in new_set.courses:
            if not any(
                old_course == new_course or old_course > new_course
                for old_course in old_set.courses
            ):
                self.new_only.append(new_course)

    def __str__(self):
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
