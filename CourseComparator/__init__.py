from .cc_classes import (
    CourseSimilarity,
    Course,
    CoursePair,
    CourseSet,
    CourseSetDelta,
)

from .cc_functions import similarity, init, query, EMPTY_SEMESTER

__all__ = [
    "CourseSimilarity",
    "Course",
    "CoursePair",
    "CourseSet",
    "CourseSetDelta",
    "similarity",
    "init",
    "query",
    "EMPTY_SEMESTER",
]

__version__ = "0.1.0"
