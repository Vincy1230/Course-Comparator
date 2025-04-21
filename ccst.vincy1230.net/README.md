# LLM-Graph (以并行迭代流程为例)

`CourseComparator 自动录入`  
CourseComparator 课程比较器用于比较不同的专业、届别或年级之间的课程设置，供转专业、降级学生确认可冲抵及需补修的课程。此处是该比较器的录入工具。

## 开始 `开始`

| 输入字段 | 变量名称 | 显示名称     | 支持文档 | 上传类型    | 最大上传数 |
| -------- | -------- | ------------ | -------- | ----------- | ---------- |
| 文件列表 | `files`  | 培养方案 PDF | 文档     | 上传 / 链接 | 10         |

## `并行迭代` 开始

输入: 开始 / files `Array[File]`  
最大并行数: 10

## `并行迭代` 分析 PDF 文件名 `代码执行`

| 输入变量 |                               |
| -------- | ----------------------------- |
| filename | 并行处理 / item.name `String` |

```python
import re

def main(filename: str) -> dict[str, str]:

    match = re.search(r"(\d{4})", filename)
    if not match:
        raise ValueError("专业信息匹配失败")

    jie = match.group(1)
    major_part = filename[: match.start()]
    major = major_part.replace("专业", "").strip()

    return {
        "major": major,
        "jie": jie,
    }

```

| 输出变量 |          |
| -------- | -------- |
| major    | `String` |
| jie      | `String` |

## `并行迭代` 分析 PDF 文件 `LLM`

#### 模型

`claude-3-7-sonnet-20250219`, 回复格式: `json`

#### SYSTEM

```markdown
## 要求

你将收到一份大学专业的培养计划 PDF，请根据培养计划中**按学期排序的**教学计划进度表，列出每学期的 `课程编码`、`课程名称`、`学分`、`课程属性`，并按学期分别输出为 `1.csv` ~ `8.csv`。

## 示例

\`\`\`csv
course_code,course_name,credit,required
MARA3G1001,高等数学（下）,4,1
FLGA4G1002,大学英语（二）,3,1
MATA4B1003,体育（一）,1,1
PHYA4B1000004,大学物理（上）,4,1
080201C0000P5,Python 语言程序设计,3,0
080702A5000C6,Java 语言程序设计,3,0
080801A2C7,中国近现代史纲要,2,1
080801A2C8,数据结构,4,1
080801D3D9,数字逻辑,3,1
\`\`\`

| course_code  | course_name  | credit | required                                 |
| ------------ | ------------ | ------ | ---------------------------------------- |
| 课程编码     | 课程名称     | 学分   | 课程属性, 1 为必修, 0 为选修 (包括专选)  |
| course_code  | course_name  | credit | required                                 |

## 注意

一份文件中可能包含多个表，可能用多种方式对开设的课程进行排序，请**仅关注按照学期排序的课程**。

如果某个学期没有任何课程，**只输出 csv 表头即可**

## 输出格式

\`\`\`json
{
"csv1": "第 1 学期的 csv 内容",
"csv2": "第 2 学期的 csv 内容",
"csv3": "第 3 学期的 csv 内容",
"csv4": "第 4 学期的 csv 内容",
"csv5": "第 5 学期的 csv 内容",
"csv6": "第 6 学期的 csv 内容",
"csv7": "第 7 学期的 csv 内容",
"csv8": "第 8 学期的 csv 内容"
}
\`\`\`
```

#### USER

并行迭代 / item `flie`

#### 输出变量

text `String`  
生成内容

## `并行迭代` 处理结构化数据 `代码执行`

| 输入变量 |          |
| -------- | -------- |
| json     | `String` |

```python
import json


def main(text: str) -> dict:
    csv_data = json.loads(text)
    csv_list = []

    for i in range(1, 9):
        csv_key = f"csv{i}"
        csv_list.append(csv_data[csv_key])

    return {
        "csv_list": csv_list,
        "csv_string": "\n###\n".join(csv_list),
    }

```

| 输出变量   |                 |
| ---------- | --------------- |
| csv_list   | `Array[String]` |
| csv_string | `String`        |

## `并行迭代` 上传至云存储 `CourseComparator 入库工具`

| 输入变量            |                             |
| ------------------- | --------------------------- |
| major `String`      | 分析 PDF 文件名 / major     |
| jie `String`        | 分析 PDF 文件名 / jie       |
| csv_string `String` | 处理结构化数据 / csv_string |

| 输出变量 |          |
| -------- | -------- |
| text     | `String` |

## `并行迭代` 构建用户输出 `模板转换`

| 输入变量 |                                           |
| -------- | ----------------------------------------- |
| major    | 分析 PDF 文件名 / major `String`          |
| jie      | 分析 PDF 文件名 / jie `String`            |
| url      | 上传至云存储 / test `String`              |
| csv_list | 处理结构化数据 / csv_list `Array[String]` |

```markdown
**_{{ major }}_** 专业  
**_{{ jie }}_** 级

识别完成，数据已归档至后台。你也可以在这里下载本次识别的数据副本：

{{ url }}

**_1.csv_**

\`\`\`csv
{{ csv_list[0] }}
\`\`\`

**_2.csv_**

\`\`\`csv
{{ csv_list[1] }}
\`\`\`

**_3.csv_**

\`\`\`csv
{{ csv_list[2] }}
\`\`\`

**_4.csv_**

\`\`\`csv
{{ csv_list[3] }}
\`\`\`

**_5.csv_**

\`\`\`csv
{{ csv_list[4] }}
\`\`\`

**_6.csv_**

\`\`\`csv
{{ csv_list[5] }}
\`\`\`

**_7.csv_**

\`\`\`csv
{{ csv_list[6] }}
\`\`\`

**_8.csv_**

\`\`\`csv
{{ csv_list[7] }}
\`\`\`
```

| 输出变量 |          |
| -------- | -------- |
| text     | `String` |

## `并行迭代` 终止

输出变量: 构建用户输出 / output `String`

## 聚合多组并行 `模板转换`

| 输入变量 |                                   |
| -------- | --------------------------------- |
| outputs  | 并行处理 / output `Array[String]` |

```markdown
{{ outputs | join('\n---\n') }}
```

| 输出变量 |          |
| -------- | -------- |
| output   | `String` |

## 结束 `结束`

| 输出变量 |                                |
| -------- | ------------------------------ |
| output   | 聚合多组并行 / output `String` |
