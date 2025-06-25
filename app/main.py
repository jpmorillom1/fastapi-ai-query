from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .models import configure_gemini, get_response, obtener_datos
import os

app = FastAPI()

#@app.on_event("startup")
#async def startup_event():
#    configure_gemini()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    df_preview = obtener_datos().head(5).to_html(classes="df-preview", index=False)
    return templates.TemplateResponse("index.html", {"request": request, "df_preview": df_preview})


@app.post("/ask", response_class=HTMLResponse)
async def ask_question(request: Request, question: str = Form(...), model: str = Form(...)):
    try:
        response, _ = get_response(question, model)
        #df_preview = obtener_datos().head(5).to_html(classes="df-preview", index=False)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "response": response,
                "question": question,
                "model": model,
                #"df_preview": df_preview
            }
        )
    except Exception as e:
        #df_preview = obtener_datos().head(5).to_html(classes="df-preview", index=False)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": str(e),
                "question": question,
                "model": model,
                #"df_preview": df_preview
            }
        )
