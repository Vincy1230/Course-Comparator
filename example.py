import CourseComparator as cc


loader = cc.init("D:\\ProjectFiles\\课程比较器\\Course-Comparator\\data")

print(cc.query(loader, "人工智能", "2021", 2) - cc.query(loader, "人工智能", "2023", 2))
