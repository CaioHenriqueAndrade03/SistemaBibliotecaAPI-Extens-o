import httpx
from fastapi import HTTPException
from config import settings

BASE_URL = settings.catalogo_api_url


def buscar_livro(livro_id: int) -> dict:
    """Consulta o catalogo-api para obter os dados de um livro."""
    try:
        resp = httpx.get(f"{BASE_URL}/livros/{livro_id}", timeout=5.0)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="catalogo-api indisponível.")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Livro não encontrado.")
    resp.raise_for_status()
    return resp.json()


def buscar_socio(socio_id: int) -> dict:
    """Consulta o catalogo-api para obter os dados de um sócio."""
    try:
        resp = httpx.get(f"{BASE_URL}/socios/{socio_id}", timeout=5.0)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="catalogo-api indisponível.")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Sócio não encontrado.")
    resp.raise_for_status()
    return resp.json()


def ajustar_estoque(livro_id: int, delta: int) -> dict:
    """Solicita ao catalogo-api que ajuste a quantidade disponível de um livro."""
    try:
        resp = httpx.patch(
            f"{BASE_URL}/livros/{livro_id}/estoque",
            json={"delta": delta},
            timeout=5.0,
        )
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="catalogo-api indisponível.")

    if resp.status_code == 400:
        raise HTTPException(status_code=400, detail=resp.json().get("detail"))
    resp.raise_for_status()
    return resp.json()


def contar_livros() -> int:
    resp = httpx.get(f"{BASE_URL}/livros/", timeout=5.0)
    resp.raise_for_status()
    return len(resp.json())


def contar_socios() -> int:
    resp = httpx.get(f"{BASE_URL}/socios/", timeout=5.0)
    resp.raise_for_status()
    return len(resp.json())
