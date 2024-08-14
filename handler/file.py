from fastapi import APIRouter
from store import store_manager

file_api = APIRouter(prefix="/file")


@file_api.get("/listdir")
async def listdir(parentPath: str):
    files = await store_manager.store.listdir(parentPath)
    return [it.to_model().model_dump(mode="json", by_alias=True) for it in files]
