from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    app = FastAPI(
        title="Mood-Weather-Music API",
        description="An API that recommends songs based on user's mood and weather in their city",
        version="1.0.0",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Import and include API router
    from app.api.endpoints import router
    app.include_router(router)
    
    # Custom OpenAPI schema
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        
        # Add more OpenAPI details as needed
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi
    
    return app
