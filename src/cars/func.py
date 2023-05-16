import asyncio
import os
from typing import List

import aiofiles
from fastapi import UploadFile


async def save_file(file_path, file_content):  # Сохраняем файл
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)
