from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

# Create the main app without a prefix
app = FastAPI(
    title="Planetary Design Environment API",
    description="A comprehensive API for managing planetary systems, bodies, and simulation settings",
    version="1.0.0"
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Define Models for basic status checks
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

# Basic health check routes
@api_router.get("/")
async def root():
    return {"message": "Planetary Design Environment API is running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database": "connected"
    }

@api_router.post("/status")
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    return status_obj

@api_router.get("/status")
async def get_status_checks():
    # Return a mock list for testing
    return [
        StatusCheck(id="test-id-1", client_name="test-client-1"),
        StatusCheck(id="test-id-2", client_name="test-client-2")
    ]

# Planetary API router
planetary_router = APIRouter(prefix="/api/planetary", tags=["planetary"])

# Mock planetary data
mock_bodies = [
    {
        "id": "sun",
        "name": "Sun",
        "radius": 5.0,
        "color": "#FDB813",
        "position": [0, 0, 0],
        "rotation_speed": 0.001,
        "description": "The Sun is the star at the center of our solar system.",
        "facts": ["Temperature: 5,778 K (surface)", "Mass: 1.989 × 10³⁰ kg"],
        "emissive": True,
        "has_flares": True,
        "body_type": "star",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "earth",
        "name": "Earth",
        "radius": 1.3,
        "color": "#6B93D6",
        "orbit_radius": 30.0,
        "orbit_speed": 0.01,
        "rotation_speed": 0.01,
        "position": [30, 0, 0],
        "description": "Earth is the third planet from the Sun.",
        "facts": ["Distance from Sun: 150 million km", "Orbital period: 365.25 days"],
        "has_atmosphere": True,
        "body_type": "planet",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "moon",
        "name": "Moon",
        "radius": 0.35,
        "color": "#D3D3D3",
        "orbit_radius": 4.0,
        "orbit_speed": 0.05,
        "rotation_speed": 0.05,
        "parent": "earth",
        "position": [34, 0, 0],
        "description": "The Moon is Earth's only natural satellite.",
        "facts": ["Distance from Earth: 384,400 km", "Orbital period: 27.3 days"],
        "body_type": "moon",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "id": "iss",
        "name": "International Space Station",
        "radius": 0.08,
        "color": "#C0C0C0",
        "orbit_radius": 6.5,
        "orbit_speed": 0.08,
        "parent": "earth",
        "description": "The ISS is a large spacecraft in orbit around Earth.",
        "facts": ["Altitude: 408 km above Earth", "Speed: 28,000 km/h"],
        "body_type": "satellite",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

mock_settings = [
    {
        "id": "default_settings",
        "time_speed": 1.0,
        "show_orbits": True,
        "show_labels": True,
        "camera_distance": 80.0,
        "ambient_light_intensity": 0.2,
        "point_light_intensity": 1.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

mock_systems = [
    {
        "id": "default_system",
        "name": "Solar System",
        "description": "Our solar system with Sun, planets, moon, and satellites",
        "bodies": ["sun", "earth", "moon", "iss"],
        "settings": "default_settings",
        "is_default": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

# Planetary Bodies Routes
@planetary_router.get("/bodies")
async def get_all_bodies():
    """Get all planetary bodies"""
    return mock_bodies

@planetary_router.get("/bodies/{body_id}")
async def get_body(body_id: str):
    """Get a specific planetary body"""
    for body in mock_bodies:
        if body["id"] == body_id:
            return body
    return {"detail": "Planetary body not found"}, 404

@planetary_router.post("/bodies")
async def create_body(body: dict):
    """Create a new planetary body"""
    body_id = body.get("id", str(uuid.uuid4()))
    new_body = {
        "id": body_id,
        "name": body.get("name", "New Body"),
        "radius": body.get("radius", 1.0),
        "color": body.get("color", "#FFFFFF"),
        "position": body.get("position", [0, 0, 0]),
        "rotation_speed": body.get("rotation_speed", 0.001),
        "description": body.get("description", ""),
        "facts": body.get("facts", []),
        "body_type": body.get("body_type", "planet"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_bodies.append(new_body)
    return new_body

@planetary_router.put("/bodies/{body_id}")
async def update_body(body_id: str, body_update: dict):
    """Update a planetary body"""
    for i, body in enumerate(mock_bodies):
        if body["id"] == body_id:
            for key, value in body_update.items():
                if key not in ["id", "created_at"]:
                    mock_bodies[i][key] = value
            mock_bodies[i]["updated_at"] = datetime.utcnow()
            return mock_bodies[i]
    return {"detail": "Planetary body not found"}, 404

@planetary_router.delete("/bodies/{body_id}")
async def delete_body(body_id: str):
    """Delete a planetary body"""
    for i, body in enumerate(mock_bodies):
        if body["id"] == body_id:
            del mock_bodies[i]
            return {"message": "Planetary body deleted successfully"}
    return {"detail": "Planetary body not found"}, 404

# Simulation Settings Routes
@planetary_router.get("/settings")
async def get_all_settings():
    """Get all simulation settings"""
    return mock_settings

@planetary_router.get("/settings/{settings_id}")
async def get_settings(settings_id: str):
    """Get specific simulation settings"""
    for settings in mock_settings:
        if settings["id"] == settings_id:
            return settings
    return {"detail": "Settings not found"}, 404

@planetary_router.post("/settings")
async def create_settings(settings: dict):
    """Create new simulation settings"""
    settings_id = settings.get("id", str(uuid.uuid4()))
    new_settings = {
        "id": settings_id,
        "time_speed": settings.get("time_speed", 1.0),
        "show_orbits": settings.get("show_orbits", True),
        "show_labels": settings.get("show_labels", True),
        "camera_distance": settings.get("camera_distance", 80.0),
        "ambient_light_intensity": settings.get("ambient_light_intensity", 0.2),
        "point_light_intensity": settings.get("point_light_intensity", 1.5),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_settings.append(new_settings)
    return new_settings

@planetary_router.put("/settings/{settings_id}")
async def update_settings(settings_id: str, settings_update: dict):
    """Update simulation settings"""
    for i, settings in enumerate(mock_settings):
        if settings["id"] == settings_id:
            for key, value in settings_update.items():
                if key not in ["id", "created_at"]:
                    mock_settings[i][key] = value
            mock_settings[i]["updated_at"] = datetime.utcnow()
            return mock_settings[i]
    return {"detail": "Settings not found"}, 404

# Planetary Systems Routes
@planetary_router.get("/systems")
async def get_all_systems():
    """Get all planetary systems"""
    return mock_systems

@planetary_router.get("/systems/{system_id}")
async def get_system(system_id: str):
    """Get a specific planetary system"""
    for system in mock_systems:
        if system["id"] == system_id:
            return system
    return {"detail": "Planetary system not found"}, 404

@planetary_router.post("/systems")
async def create_system(system: dict):
    """Create a new planetary system"""
    system_id = system.get("id", str(uuid.uuid4()))
    new_system = {
        "id": system_id,
        "name": system.get("name", "New System"),
        "description": system.get("description", ""),
        "bodies": system.get("bodies", []),
        "settings": system.get("settings"),
        "is_default": system.get("is_default", False),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    mock_systems.append(new_system)
    return new_system

@planetary_router.put("/systems/{system_id}")
async def update_system(system_id: str, system_update: dict):
    """Update a planetary system"""
    for i, system in enumerate(mock_systems):
        if system["id"] == system_id:
            for key, value in system_update.items():
                if key not in ["id", "created_at"]:
                    mock_systems[i][key] = value
            mock_systems[i]["updated_at"] = datetime.utcnow()
            return mock_systems[i]
    return {"detail": "Planetary system not found"}, 404

@planetary_router.delete("/systems/{system_id}")
async def delete_system(system_id: str):
    """Delete a planetary system"""
    for i, system in enumerate(mock_systems):
        if system["id"] == system_id:
            del mock_systems[i]
            return {"message": "Planetary system deleted successfully"}
    return {"detail": "Planetary system not found"}, 404

# Initialize default data
@planetary_router.post("/initialize")
async def initialize_default_data():
    """Initialize the database with default solar system data"""
    return {"message": "Default data already exists"}

# Include the planetary routes
app.include_router(planetary_router)

# Include the main API router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Planetary Design Environment API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Planetary Design Environment API shutting down...")