from fastapi import APIRouter
from store import store_manager

file_api = APIRouter(prefix="/file")


@file_api.get("/listdir")
async def listdir(parent_path: str):
    files = await store_manager.store.listdir(parent_path)
    return [it.to_model().model_dump(mode="json") for it in files]
