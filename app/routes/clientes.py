from fastapi import APIRouter

router = APIRouter(prefix="/clientes")


@router.post("/nuevo")
async def cargar_cliente():
    return

@router.get("/listar")
async def listar_clientes():
    return