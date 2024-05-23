from fastapi import APIRouter

router = APIRouter(prefix="/kayaks")


@router.post("/cargar")
async def cargar_kayak():
    return

@router.get("/listar")
async def listar_kayak():
    return