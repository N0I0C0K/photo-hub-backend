from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from store import store_manager
from store.backend.aliyun import login_use_redirect


from handler.file import file_api

app = FastAPI(on_startup=[store_manager.setup])
app.include_router(file_api)


@app.get("/login")
async def login():
    return RedirectResponse(login_use_redirect("http://127.0.0.1:8110/login-redirect"))


@app.get("/login-redirect")
async def login_redirect(code: str):
    print(code)
    return {"code": code}
