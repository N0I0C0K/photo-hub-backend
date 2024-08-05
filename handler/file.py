from fastapi import APIRouter

file_api = APIRouter(prefix="/file")


@file_api.get("/listdir")
async def listdir(parent_path: str):
    pass
