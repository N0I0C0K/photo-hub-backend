from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from aliyun.login import login_use_redirect

app = FastAPI()


@app.get("/login")
async def login():
    return RedirectResponse(login_use_redirect("http://127.0.0.1:8110/login-redirect"))


@app.get("/login-redirect")
async def login_redirect(code: str):
    print(code)
    return {"code": code}
