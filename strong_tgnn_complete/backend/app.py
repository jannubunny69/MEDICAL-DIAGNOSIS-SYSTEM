from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from .routes import patients, visits, inference, snapshots, fusion, report
import os
import base64

app = FastAPI(title="strong_tgnn backend")

# API routers
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(visits.router, prefix="/visits", tags=["visits"])
app.include_router(inference.router, prefix="/inference", tags=["inference"])
app.include_router(snapshots.router, prefix="/snapshots", tags=["snapshots"])
app.include_router(fusion.router, prefix="/fusion", tags=["fusion"])
app.include_router(report.router, prefix="/report", tags=["report"])

# Serve frontend static files from the `frontend` folder at /static
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
STATIC_DIR = os.path.join(FRONTEND_DIR, 'static')
if os.path.isdir(STATIC_DIR):
    app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')

@app.get('/')
async def serve_main():
    return RedirectResponse(url='/main.html')

@app.get('/index.html')
async def serve_index():
    idx = os.path.join(FRONTEND_DIR, 'index.html')
    if os.path.isfile(idx):
        return FileResponse(idx, media_type='text/html')
    return {"message": "index not found"}

@app.get('/favicon.ico')
async def favicon():
    fav = os.path.join(STATIC_DIR, 'favicon.ico')
    if os.path.isfile(fav):
        return FileResponse(fav, media_type='image/x-icon')
    png_base64 = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAUVBMVEUAAAD///////////////////////////////////////////////////////////////////////////////////////////////////9k3r4WAAAAH3RSTlMAAQIDBAUGBwgJCgsMDQ4PEBESExQVFhcYGRobHB0eHyAhI+4pXQAAAF1JREFUGNNjYIASJiYmBgYGBgYGBgYGBgZGBgYGBkaGhoZGQkJCAgICQkJCQkJCAgICQkJCVkA2CkEAAQwGJYl3QvMAAAAASUVORK5CYII="
    )
    data = base64.b64decode(png_base64)
    return Response(content=data, media_type='image/png')

@app.get('/{page}.html')
async def serve_page(page: str):
    if '/' in page or '\\' in page:
        return {"detail": "invalid page"}
    candidate = os.path.join(FRONTEND_DIR, f"{page}.html")
    if os.path.isfile(candidate):
        return FileResponse(candidate, media_type='text/html')
    return {"detail": "not found"}


# Server start block
if __name__ == "__main__":
    import threading, webbrowser
    def open_main_html():
        import time
        time.sleep(2)
        webbrowser.open('http://localhost:8000/main.html')
    threading.Thread(target=open_main_html).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
