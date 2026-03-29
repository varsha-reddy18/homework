from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# =========================
# IMPORT YOUR ROUTERS
# =========================
from app.routes.auth_routes import router as auth_router
from app.routes.ask_routes import router as ask_router
from app.routes.image_routes import router as image_router
from app.routes.grammar_routes import router as grammar_router

# =========================
# LIFESPAN — pre-warm models on startup
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        from app.services.ai_service import model as ai_model
    except Exception as e:
        print("⚠️ AI model load skipped:", e)

    try:
        from app.services.grammar_service import grammar_model
    except Exception as e:
        print("⚠️ Grammar model load skipped:", e)

    print("✅ App started successfully.")
    yield
    print("🛑 Shutting down.")

# =========================
# APP
# =========================
app = FastAPI(lifespan=lifespan)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# =========================
# STATIC FILES
# =========================
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# =========================
# INCLUDE API ROUTES
# =========================
app.include_router(auth_router)
app.include_router(ask_router)
app.include_router(image_router)
app.include_router(grammar_router)

# =========================
# PAGE ROUTES
# =========================
@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/login-page")
def login_page():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/signup-page")
def signup_page():
    return FileResponse(os.path.join(STATIC_DIR, "signup.html"))

@app.get("/dashboard")
def dashboard_page():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

@app.get("/login.html")
def login_html():
    return FileResponse(os.path.join(STATIC_DIR, "login.html"))

@app.get("/signup.html")
def signup_html():
    return FileResponse(os.path.join(STATIC_DIR, "signup.html"))

@app.get("/dashboard.html")
def dashboard_html():
    return FileResponse(os.path.join(STATIC_DIR, "dashboard.html"))

# Optional direct static shortcuts (if needed)
@app.get("/css/{file_path:path}")
def serve_css(file_path: str):
    return FileResponse(os.path.join(STATIC_DIR, "css", file_path))

@app.get("/js/{file_path:path}")
def serve_js(file_path: str):
    return FileResponse(os.path.join(STATIC_DIR, "js", file_path))

@app.get("/images/{file_path:path}")
def serve_images(file_path: str):
    return FileResponse(os.path.join(STATIC_DIR, "images", file_path))

# Suppress favicon error
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    ico = os.path.join(STATIC_DIR, "favicon.ico")
    if os.path.exists(ico):
        return FileResponse(ico)
    return JSONResponse({}, status_code=204)

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}