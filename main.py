from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import account_routes, analytics_routes, auth_routes

app = FastAPI(title="Portfolio Performance API")

# CORS SETTINGS
origins = [
    "*",  # allow all (good for development)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(account_routes.router)
app.include_router(analytics_routes.router)
app.include_router(auth_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="192.168.0.117", port=8001, reload=True)



#8377