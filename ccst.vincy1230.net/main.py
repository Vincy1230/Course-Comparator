import os
import json
import zipfile
import csv
from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse, FileResponse
from pydantic import BaseModel
from service.auth import verify_token
from pathlib import Path

BASE_DIR = str(os.getenv("BASE_DIR"))
BASE_URL = str(os.getenv("BASE_URL"))


class DataInput(BaseModel):
    major: str
    jie: str
    csv_string: str


app = FastAPI()


@app.post("/upload", dependencies=[Depends(verify_token)])
def upload(data: DataInput) -> PlainTextResponse:
    csv_list = data.csv_string.split("###")

    # 创建目标目录
    target_dir = Path(BASE_DIR) / data.major / data.jie
    target_dir.mkdir(parents=True, exist_ok=True)

    # 创建 zip 文件目录
    zip_dir = Path(BASE_DIR) / "zips"
    zip_dir.mkdir(parents=True, exist_ok=True)

    # 创建 summary 目录
    summary_dir = Path(BASE_DIR) / "summary"
    summary_dir.mkdir(parents=True, exist_ok=True)

    # 写入 CSV 文件并准备 zip 文件
    zip_path = zip_dir / f"{data.major}.{data.jie}.zip"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for i in range(1, 9):

            # 写入单个 CSV 文件
            csv_path = target_dir / f"{i}.csv"
            with open(csv_path, "w", encoding="GBK") as f:
                f.write(csv_list[i - 1].strip())

            # 添加到 zip 文件
            zipf.write(csv_path, f"{i}.csv")

    # 生成总表
    summary_path = summary_dir / f"{data.major}.{data.jie}.csv"
    with open(summary_path, "w", encoding="GBK", newline="") as summary_file:
        writer = csv.writer(summary_file)

        # 写入表头
        first_csv = csv_list[0].strip()
        header = ["semester"] + first_csv.split("\n")[0].split(",")
        writer.writerow(header)

        # 写入数据
        for i in range(1, 9):
            semester_data = csv_list[i - 1].strip().split("\n")
            if len(semester_data) <= 1:  # 只有表头或空文件
                continue

            for row in semester_data[1:]:  # 跳过表头
                if row.strip():  # 确保行不为空
                    writer.writerow([i] + row.split(","))

    # 返回下载链接
    download_url = f"> zip 副本下载链接  \n"
    download_url += f"[{BASE_URL}/zips/{data.major}.{data.jie}.zip]({BASE_URL}/zips/{data.major}.{data.jie}.zip)  \n"
    download_url += f"> csv总表下载链接  \n"
    download_url += f"[{BASE_URL}/summary/{data.major}.{data.jie}.csv]({BASE_URL}/summary/{data.major}.{data.jie}.csv)"
    return PlainTextResponse(download_url)


@app.get("/")
async def root():
    return {
        "message": "Hello World",
    }


if os.path.exists("./favicon.ico"):

    @app.get("/favicon.ico")
    async def get_favicon():
        return FileResponse("./favicon.ico")
