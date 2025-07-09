from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class PlanetaryBody(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    radius: float
    color: str
    position: List[float] = Field(default_factory=lambda: [0, 0, 0])
    rotation_speed: float = 0.001
    description: str = ""
    facts: List[str] = Field(default_factory=list)
    texture: Optional[str] = None
    emissive: bool = False
    has_flares: bool = False
    has_atmosphere: bool = False
    orbit_radius: Optional[float] = None
    orbit_speed: Optional[float] = None
    parent: Optional[str] = None
    body_type: str = "planet"  # planet, moon, satellite, star
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PlanetaryBodyCreate(BaseModel):
    name: str
    radius: float
    color: str
    position: List[float] = Field(default_factory=lambda: [0, 0, 0])
    rotation_speed: float = 0.001
    description: str = ""
    facts: List[str] = Field(default_factory=list)
    texture: Optional[str] = None
    emissive: bool = False
    has_flares: bool = False
    has_atmosphere: bool = False
    orbit_radius: Optional[float] = None
    orbit_speed: Optional[float] = None
    parent: Optional[str] = None
    body_type: str = "planet"

class PlanetaryBodyUpdate(BaseModel):
    name: Optional[str] = None
    radius: Optional[float] = None
    color: Optional[str] = None
    position: Optional[List[float]] = None
    rotation_speed: Optional[float] = None
    description: Optional[str] = None
    facts: Optional[List[str]] = None
    texture: Optional[str] = None
    emissive: Optional[bool] = None
    has_flares: Optional[bool] = None
    has_atmosphere: Optional[bool] = None
    orbit_radius: Optional[float] = None
    orbit_speed: Optional[float] = None
    parent: Optional[str] = None
    body_type: Optional[str] = None

class SimulationSettings(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    time_speed: float = 1.0
    show_orbits: bool = True
    show_labels: bool = True
    camera_distance: float = 80.0
    ambient_light_intensity: float = 0.2
    point_light_intensity: float = 1.5
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class SimulationSettingsCreate(BaseModel):
    user_id: Optional[str] = None
    time_speed: float = 1.0
    show_orbits: bool = True
    show_labels: bool = True
    camera_distance: float = 80.0
    ambient_light_intensity: float = 0.2
    point_light_intensity: float = 1.5

class SimulationSettingsUpdate(BaseModel):
    time_speed: Optional[float] = None
    show_orbits: Optional[bool] = None
    show_labels: Optional[bool] = None
    camera_distance: Optional[float] = None
    ambient_light_intensity: Optional[float] = None
    point_light_intensity: Optional[float] = None

class PlanetarySystem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    user_id: Optional[str] = None
    bodies: List[str] = Field(default_factory=list)  # List of PlanetaryBody IDs
    settings: Optional[str] = None  # SimulationSettings ID
    is_default: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PlanetarySystemCreate(BaseModel):
    name: str
    description: str = ""
    user_id: Optional[str] = None
    bodies: List[str] = Field(default_factory=list)
    settings: Optional[str] = None
    is_default: bool = False

class PlanetarySystemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    bodies: Optional[List[str]] = None
    settings: Optional[str] = None
    is_default: Optional[bool] = None