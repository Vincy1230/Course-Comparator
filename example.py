# 导入课程比较器模块
import CourseComparator as cc

# 传入数据集根目录，初始化数据加载器
loader = cc.init("<数据集根目录>")

# 获取旧的课程方案
old_courses = loader("人工智能", "2021", 4)

# 获取新的课程方案
new_courses = loader("人工智能", "2023", 4)

# 打印两个方案的差异
print(old_courses - new_courses)
