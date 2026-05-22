from fastapi import FastAPI
from routes.dashboard import dashboard_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(dashboard_router, prefix="/dashboard")

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
