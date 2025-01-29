from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import router as app_router
from fastapi.responses import HTMLResponse
app = FastAPI()

# Incluir rutas del proyecto
app.include_router(app_router)

# Montar la carpeta de plantillas como fuente de archivos estáticos
app.mount("/", StaticFiles(directory="templates"), name="templates")

# Configurar plantillas
templates = Jinja2Templates(directory="templates")

@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/recommend")
async def recommend(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})

@app.get("/perfil")
async def perfil(request: Request):
    return templates.TemplateResponse("perfil.html", {"request": request})

@app.get("/contacte")
async def contacte(request: Request):
    return templates.TemplateResponse("contacte.html", {"request": request})

@app.get("/resultados")
async def resultados(request: Request):
    return templates.TemplateResponse("resultados.html", {"request": request})
