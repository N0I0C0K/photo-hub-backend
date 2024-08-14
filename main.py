from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from store import store_manager
from store.backend.aliyun.login import login_use_redirect


from handler.file import file_api

from config import save_config


async def store_save():
    await store_manager.dispose()
    save_config()


app = FastAPI(on_startup=[store_manager.setup], on_shutdown=[store_save])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_api)


@app.get("/login-redirect")
async def login_redirect(code: str):
    print(code)
    return {"code": code}


@app.get("/test")
async def refresh_token():
    await store_manager.store._refresh_token()
