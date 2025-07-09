from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Optional
from datetime import datetime
import os

from ..models.planetary_models import (
    PlanetaryBody, PlanetaryBodyCreate, PlanetaryBodyUpdate,
    SimulationSettings, SimulationSettingsCreate, SimulationSettingsUpdate,
    PlanetarySystem, PlanetarySystemCreate, PlanetarySystemUpdate
)

router = APIRouter(prefix="/api/planetary", tags=["planetary"])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Planetary Bodies Routes
@router.get("/bodies", response_model=List[PlanetaryBody])
async def get_all_bodies():
    """Get all planetary bodies"""
    bodies = await db.planetary_bodies.find().to_list(1000)
    return [PlanetaryBody(**body) for body in bodies]

@router.get("/bodies/{body_id}", response_model=PlanetaryBody)
async def get_body(body_id: str):
    """Get a specific planetary body"""
    body = await db.planetary_bodies.find_one({"id": body_id})
    if not body:
        raise HTTPException(status_code=404, detail="Planetary body not found")
    return PlanetaryBody(**body)

@router.post("/bodies", response_model=PlanetaryBody)
async def create_body(body: PlanetaryBodyCreate):
    """Create a new planetary body"""
    body_dict = body.dict()
    body_obj = PlanetaryBody(**body_dict)
    await db.planetary_bodies.insert_one(body_obj.dict())
    return body_obj

@router.put("/bodies/{body_id}", response_model=PlanetaryBody)
async def update_body(body_id: str, body_update: PlanetaryBodyUpdate):
    """Update a planetary body"""
    existing_body = await db.planetary_bodies.find_one({"id": body_id})
    if not existing_body:
        raise HTTPException(status_code=404, detail="Planetary body not found")
    
    update_data = body_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.planetary_bodies.update_one(
        {"id": body_id},
        {"$set": update_data}
    )
    
    updated_body = await db.planetary_bodies.find_one({"id": body_id})
    return PlanetaryBody(**updated_body)

@router.delete("/bodies/{body_id}")
async def delete_body(body_id: str):
    """Delete a planetary body"""
    result = await db.planetary_bodies.delete_one({"id": body_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Planetary body not found")
    return {"message": "Planetary body deleted successfully"}

# Simulation Settings Routes
@router.get("/settings", response_model=List[SimulationSettings])
async def get_all_settings():
    """Get all simulation settings"""
    settings = await db.simulation_settings.find().to_list(1000)
    return [SimulationSettings(**setting) for setting in settings]

@router.get("/settings/{settings_id}", response_model=SimulationSettings)
async def get_settings(settings_id: str):
    """Get specific simulation settings"""
    settings = await db.simulation_settings.find_one({"id": settings_id})
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return SimulationSettings(**settings)

@router.post("/settings", response_model=SimulationSettings)
async def create_settings(settings: SimulationSettingsCreate):
    """Create new simulation settings"""
    settings_dict = settings.dict()
    settings_obj = SimulationSettings(**settings_dict)
    await db.simulation_settings.insert_one(settings_obj.dict())
    return settings_obj

@router.put("/settings/{settings_id}", response_model=SimulationSettings)
async def update_settings(settings_id: str, settings_update: SimulationSettingsUpdate):
    """Update simulation settings"""
    existing_settings = await db.simulation_settings.find_one({"id": settings_id})
    if not existing_settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    
    update_data = settings_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.simulation_settings.update_one(
        {"id": settings_id},
        {"$set": update_data}
    )
    
    updated_settings = await db.simulation_settings.find_one({"id": settings_id})
    return SimulationSettings(**updated_settings)

# Planetary Systems Routes
@router.get("/systems", response_model=List[PlanetarySystem])
async def get_all_systems():
    """Get all planetary systems"""
    systems = await db.planetary_systems.find().to_list(1000)
    return [PlanetarySystem(**system) for system in systems]

@router.get("/systems/{system_id}", response_model=PlanetarySystem)
async def get_system(system_id: str):
    """Get a specific planetary system"""
    system = await db.planetary_systems.find_one({"id": system_id})
    if not system:
        raise HTTPException(status_code=404, detail="Planetary system not found")
    return PlanetarySystem(**system)

@router.post("/systems", response_model=PlanetarySystem)
async def create_system(system: PlanetarySystemCreate):
    """Create a new planetary system"""
    system_dict = system.dict()
    system_obj = PlanetarySystem(**system_dict)
    await db.planetary_systems.insert_one(system_obj.dict())
    return system_obj

@router.put("/systems/{system_id}", response_model=PlanetarySystem)
async def update_system(system_id: str, system_update: PlanetarySystemUpdate):
    """Update a planetary system"""
    existing_system = await db.planetary_systems.find_one({"id": system_id})
    if not existing_system:
        raise HTTPException(status_code=404, detail="Planetary system not found")
    
    update_data = system_update.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    await db.planetary_systems.update_one(
        {"id": system_id},
        {"$set": update_data}
    )
    
    updated_system = await db.planetary_systems.find_one({"id": system_id})
    return PlanetarySystem(**updated_system)

@router.delete("/systems/{system_id}")
async def delete_system(system_id: str):
    """Delete a planetary system"""
    result = await db.planetary_systems.delete_one({"id": system_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Planetary system not found")
    return {"message": "Planetary system deleted successfully"}

# Initialize default data
@router.post("/initialize")
async def initialize_default_data():
    """Initialize the database with default solar system data"""
    
    # Check if default data already exists
    existing_bodies = await db.planetary_bodies.count_documents({})
    if existing_bodies > 0:
        return {"message": "Default data already exists"}
    
    # Default planetary bodies
    default_bodies = [
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
            "body_type": "star"
        },
        {
            "id": "mercury",
            "name": "Mercury",
            "radius": 0.8,
            "color": "#8C7853",
            "orbit_radius": 15.0,
            "orbit_speed": 0.02,
            "rotation_speed": 0.005,
            "position": [15, 0, 0],
            "description": "Mercury is the smallest planet in our solar system.",
            "facts": ["Distance from Sun: 58 million km", "Orbital period: 88 Earth days"],
            "body_type": "planet"
        },
        {
            "id": "venus",
            "name": "Venus",
            "radius": 1.2,
            "color": "#FFC649",
            "orbit_radius": 22.0,
            "orbit_speed": 0.015,
            "rotation_speed": -0.002,
            "position": [22, 0, 0],
            "description": "Venus is the second planet from the Sun.",
            "facts": ["Distance from Sun: 108 million km", "Orbital period: 225 Earth days"],
            "body_type": "planet"
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
            "body_type": "planet"
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
            "body_type": "moon"
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
            "body_type": "satellite"
        },
        {
            "id": "hubble",
            "name": "Hubble Space Telescope",
            "radius": 0.06,
            "color": "#4A90E2",
            "orbit_radius": 7.2,
            "orbit_speed": 0.06,
            "parent": "earth",
            "description": "The Hubble Space Telescope is a space-based observatory.",
            "facts": ["Altitude: 547 km above Earth", "Launch: April 24, 1990"],
            "body_type": "satellite"
        },
        {
            "id": "gps",
            "name": "GPS Satellite",
            "radius": 0.05,
            "color": "#FFD700",
            "orbit_radius": 8.5,
            "orbit_speed": 0.04,
            "parent": "earth",
            "description": "GPS satellites provide global positioning services.",
            "facts": ["Altitude: 20,200 km above Earth", "Constellation: 24+ satellites"],
            "body_type": "satellite"
        }
    ]
    
    # Insert default bodies
    for body_data in default_bodies:
        body_obj = PlanetaryBody(**body_data)
        await db.planetary_bodies.insert_one(body_obj.dict())
    
    # Create default settings
    default_settings = SimulationSettings(
        id="default_settings",
        time_speed=1.0,
        show_orbits=True,
        show_labels=True,
        camera_distance=80.0,
        ambient_light_intensity=0.2,
        point_light_intensity=1.5
    )
    await db.simulation_settings.insert_one(default_settings.dict())
    
    # Create default system
    default_system = PlanetarySystem(
        id="default_system",
        name="Solar System",
        description="Our solar system with Sun, planets, moon, and satellites",
        bodies=[body["id"] for body in default_bodies],
        settings="default_settings",
        is_default=True
    )
    await db.planetary_systems.insert_one(default_system.dict())
    
    return {"message": "Default data initialized successfully"}