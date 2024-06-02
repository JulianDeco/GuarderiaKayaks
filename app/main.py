from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes.autenticacion import router as autenticacion
from app.routes.kayaks import router as kayaks
from app.routes.clientes import router as clientes

# from app.providers.database import SessionLocal, engine, Base

# from sqlalchemy.orm import Session

titulo = "SysKayaks"
descripcion = """
Sistema para carga de clientes y kayaks de clientes, además de login de los operarios del sistema con autenticación JWT
"""

app = FastAPI(title = titulo, description=descripcion)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")



# try:
#     Base.metadata.create_all(bind=engine)
# except Exception as err:
#     print(err.args)
    
# def get_db():
    
#     try:
#         db = SessionLocal()
#         yield db
#     except Exception as error:
#         print(error.args)
#     finally: 
#         db.close()

@app.get("/ping")
async def pong():
    return {"estado":"pong"}

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )


app.include_router(autenticacion)
app.include_router(kayaks)
app.include_router(clientes)