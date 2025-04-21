# Course-Comparator 课程比较器

用于比较不同的专业、届别或年级之间的课程设置，供转专业、降级学生确认可冲抵及需补修的课程。

## 使用方法

### 整理数据集

将各个课程的数据集按照如下格式整理：

`<数据集根目录>` / `<专业>` / `<届别>` / `<学期>.csv`

例如，人工智能专业 2021 级第 1 ~ 8 学期的课程数据位于，分别存于：

`<数据集根目录>` / `人工智能` / `2021` / `1.csv`  
`<数据集根目录>` / `人工智能` / `2021` / `2.csv`  
...  
`<数据集根目录>` / `人工智能` / `2021` / `8.csv`

csv 文件的格式如下：

| csv 表头    | 含义     | 示例             | 备注                   |
| ----------- | -------- | ---------------- | ---------------------- |
| course_code | 课程代码 | `MATA5B1001`     | 将解析为字符串         |
| course_name | 课程名称 | `高等数学（上）` | 将解析为字符串         |
| credit      | 课程学分 | `5`              | 将解析为浮点数         |
| required    | 是否必修 | `1`              | `1` 为必修，`0` 为选修 |

```csv
course_code,course_name,credit,required
MATA5B1001,高等数学（上）,5,1
...
```

### 安装本软件包

```bash
pip install CourseComparator
```

### 运行程序

```python
# 导入课程比较器模块
import CourseComparator as cc

# 传入数据集根目录，初始化数据加载器
loader = cc.init("<数据集根目录>")

# 或：传入网络接口的 base_url 和 token，初始化为网络数据加载器
# loader = cc.init_internet(
#     "<base_url>",
#     "<your_token_here>",
#     "./__cc_cache__",
# )

# 获取旧的课程方案
old_courses = loader("<专业>", "<届别>", <学期>)

# 获取新的课程方案
new_courses = loader("<专业>", "<届别>", <学期>)

# 打印两个方案的差异
print(old_courses - new_courses)
```
