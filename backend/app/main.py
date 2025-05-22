# app/main.py

# =======================================================================================================
# --- Importações ---                                                                               #####
# =======================================================================================================

from fastapi import FastAPI
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware 

from app.core.config import settings
from app.api.v1.endpoints import auth as auth_router
from app.api.v1.endpoints import users_admin as users_admin_router


# =======================================================================================================
# --- Instância ---                                                                                 #####
# =======================================================================================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="FastAPI Template para CRUD",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# =======================================================================================================
# --- Configuração CORS ---                                                                         ##### 
# =======================================================================================================

origins = [
    "http://localhost",         
    "http://localhost:8080",    
    "http://localhost:5173",
    "http://localhost:5174",    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    
    allow_headers=["*"],    
)

# =======================================================================================================
# --- Rotas ---                                                                                     #####
# =======================================================================================================

app.include_router(auth_router.router, prefix=settings.API_V1_STR + "/auth", tags=["Authentication & Users"])
app.include_router(users_admin_router.router, prefix=settings.API_V1_STR + "/users", tags=["Admin - Users Management"]) 

# =======================================================================================================
# --- Endpoints ---                                                                                 #####
# =======================================================================================================

@app.get("/", tags=["Root"])
async def read_root() -> Dict[str, str]:
    """
    Endpoint raiz da aplicação.
    Retorna uma mensagem de boas-vindas.
    """
    return {"message": f"Bem-vindo à API: {settings.PROJECT_NAME}!"}

@app.get("/health", tags=["Health Check"])
async def health_check() -> Dict[str, str]:
    """
    Endpoint de verificação de saúde.
    Útil para K8s, Docker Swarm, etc.
    """
    return {"status": "ok"}
