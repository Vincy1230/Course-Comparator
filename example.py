# 导入课程比较器模块
import CourseComparator as cc

# 传入数据集根目录，初始化数据加载器
loader = cc.init("./data")

# 获取旧的课程方案
old_courses = loader("示例", "2022", 4)

# 获取新的课程方案
new_courses = loader("示例", "2023", 4)

# 打印两个方案的差异
print(old_courses - new_courses)
