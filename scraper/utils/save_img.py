import aiofiles
import httpx
from random import choices
import string
from pathlib import Path
from config.app import AppConfig


async def save_image(image_img_src: str) -> str:
    file_name = "".join(choices(string.ascii_letters + string.digits, k=30)) + ".jpg"
    dirs = AppConfig.PICTURES_DIRECTORY.split("/")
    for dir_count in range(len(dirs)):
        Path(
            f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{"/".join(dirs[0:dir_count+1])}"
        ).mkdir(parents=True, exist_ok=True)

    async with httpx.AsyncClient() as aclient:
        resp = await aclient.get(image_img_src, timeout=120.0)
        if resp.status_code == 200:
            f = await aiofiles.open(
                f"{AppConfig.PARENT_DIRECTORY_PROJECTS_MAIN_FILE}/{AppConfig.PICTURES_DIRECTORY}/{file_name}",
                mode="wb",
            )
            await f.write(resp.read())
            await f.close()

    return file_name


import asyncio
