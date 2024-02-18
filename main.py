from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from prisma import Prisma


app = FastAPI(debug=True)
prisma = Prisma()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates", autoescape=False, auto_reload=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.get("/config", response_class=HTMLResponse)
async def config(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("config/config.html", context)


@app.get("/showCountries", response_class=HTMLResponse)
async def showCountries(request: Request):
    context = {"request": request}
    await prisma.connect()
    countries = await prisma.country.find_many()
    await prisma.disconnect()
    return templates.TemplateResponse(
        "config/paises/paises.html", {"request": context, "countries": countries}
    )


@app.get("/showMercados", response_class=HTMLResponse)
async def showMercados(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("config/mercados/mercados.html", context)


@app.get("/modal", response_class=HTMLResponse)
async def modal(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("config/paises/modal.html", context)


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=3000)
