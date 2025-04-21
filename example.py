# 导入课程比较器模块
import CourseComparator as cc

# 初始化数据加载器
loader = cc.init("D:\\ProjectFiles\\课程比较器\\Course-Comparator\\data")

# 打印两个方案的差异
print(loader("人工智能", "2021", 8) - loader("人工智能", "2023", 8))
