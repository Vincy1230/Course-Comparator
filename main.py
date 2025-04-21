import os
import CourseComparator as cc  # pip install CourseComparator

current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")

if os.path.exists(data_dir) and os.path.isdir(data_dir):
    print(f"已识别到数据集目录 {data_dir}")
else:
    data_path = input("请输入数据集路径: ")
    print(f"已设置数据集路径: {data_path}")
    data_dir = data_path

loader = cc.init(data_dir)

print("\n请依次输入专业、届别、学期。例如，人工智能专业 2021 级第 4 学期，输入：")
print("人工智能 2021 4 \n")

old_courses = input("请输入旧专业：").split(" ")
new_courses = input("请输入新专业：").split(" ")

old_courses = loader(old_courses[0], old_courses[1], int(old_courses[2]))
new_courses = loader(new_courses[0], new_courses[1], int(new_courses[2]))

print(old_courses - new_courses)
input("\n按回车键退出... ")
