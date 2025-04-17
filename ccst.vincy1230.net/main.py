import os
import json
import zipfile
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

    # 返回下载链接
    download_url = f"{BASE_URL}/zips/{data.major}.{data.jie}.zip"
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
