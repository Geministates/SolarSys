// Mock data for planetary system
export const planetaryData = {
  sun: {
    id: 'sun',
    name: 'Sun',
    radius: 5,
    color: '#FDB813',
    position: [0, 0, 0],
    rotationSpeed: 0.001,
    description: 'The Sun is the star at the center of our solar system. It is a nearly perfect sphere of hot plasma, heated to incandescence by nuclear fusion reactions in its core.',
    facts: [
      'Temperature: 5,778 K (surface)',
      'Mass: 1.989 × 10³⁰ kg',
      'Diameter: 1.39 million km',
      'Age: 4.6 billion years'
    ],
    texture: '/textures/sun.jpg',
    emissive: true,
    hasFlares: true
  },
  mercury: {
    id: 'mercury',
    name: 'Mercury',
    radius: 0.8,
    color: '#8C7853',
    orbitRadius: 15,
    orbitSpeed: 0.02,
    rotationSpeed: 0.005,
    position: [15, 0, 0],
    description: 'Mercury is the smallest planet in our solar system and the closest to the Sun. It has extreme temperature variations.',
    facts: [
      'Distance from Sun: 58 million km',
      'Orbital period: 88 Earth days',
      'Day length: 59 Earth days',
      'No atmosphere'
    ],
    texture: '/textures/mercury.jpg'
  },
  venus: {
    id: 'venus',
    name: 'Venus',
    radius: 1.2,
    color: '#FFC649',
    orbitRadius: 22,
    orbitSpeed: 0.015,
    rotationSpeed: -0.002,
    position: [22, 0, 0],
    description: 'Venus is the second planet from the Sun and the hottest planet in our solar system due to its thick, toxic atmosphere.',
    facts: [
      'Distance from Sun: 108 million km',
      'Orbital period: 225 Earth days',
      'Day length: 243 Earth days',
      'Thick CO₂ atmosphere'
    ],
    texture: '/textures/venus.jpg'
  },
  earth: {
    id: 'earth',
    name: 'Earth',
    radius: 1.3,
    color: '#6B93D6',
    orbitRadius: 30,
    orbitSpeed: 0.01,
    rotationSpeed: 0.01,
    position: [30, 0, 0],
    description: 'Earth is the third planet from the Sun and the only known planet to support life. It has a diverse ecosystem and liquid water.',
    facts: [
      'Distance from Sun: 150 million km',
      'Orbital period: 365.25 days',
      'Day length: 24 hours',
      'Atmosphere: 78% N₂, 21% O₂'
    ],
    texture: '/textures/earth.jpg',
    hasAtmosphere: true
  },
  moon: {
    id: 'moon',
    name: 'Moon',
    radius: 0.35,
    color: '#D3D3D3',
    orbitRadius: 4,
    orbitSpeed: 0.05,
    rotationSpeed: 0.05,
    parent: 'earth',
    position: [34, 0, 0],
    description: 'The Moon is Earth\'s only natural satellite. It influences Earth\'s tides and has been a subject of human fascination for millennia.',
    facts: [
      'Distance from Earth: 384,400 km',
      'Orbital period: 27.3 days',
      'Tidally locked to Earth',
      'Diameter: 3,474 km'
    ],
    texture: '/textures/moon.jpg'
  }
};

export const satelliteData = {
  iss: {
    id: 'iss',
    name: 'International Space Station',
    radius: 0.08,
    color: '#C0C0C0',
    orbitRadius: 6.5,
    orbitSpeed: 0.08,
    parent: 'earth',
    description: 'The International Space Station is a large spacecraft in orbit around Earth.',
    facts: [
      'Altitude: 408 km above Earth',
      'Speed: 28,000 km/h',
      'Crew: 3-6 astronauts',
      'Launched: 1998'
    ]
  },
  hubble: {
    id: 'hubble',
    name: 'Hubble Space Telescope',
    radius: 0.06,
    color: '#4A90E2',
    orbitRadius: 7.2,
    orbitSpeed: 0.06,
    parent: 'earth',
    description: 'The Hubble Space Telescope is a space-based observatory that has revolutionized astronomy.',
    facts: [
      'Altitude: 547 km above Earth',
      'Launch: April 24, 1990',
      'Mirror diameter: 2.4 meters',
      'Images taken: Over 1.5 million'
    ]
  },
  gps: {
    id: 'gps',
    name: 'GPS Satellite',
    radius: 0.05,
    color: '#FFD700',
    orbitRadius: 8.5,
    orbitSpeed: 0.04,
    parent: 'earth',
    description: 'GPS satellites provide global positioning and navigation services.',
    facts: [
      'Altitude: 20,200 km above Earth',
      'Constellation: 24+ satellites',
      'Orbit period: 12 hours',
      'Accuracy: Within 3 meters'
    ]
  }
};

export const simulationSettings = {
  timeSpeed: 1,
  showOrbits: true,
  showLabels: true,
  cameraDistance: 80,
  ambientLightIntensity: 0.2,
  pointLightIntensity: 1.5
};

export const textureUrls = {
  sun: 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=1024&q=80',
  mercury: 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=512&q=80',
  venus: 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=512&q=80',
  earth: 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=512&q=80',
  moon: 'https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=512&q=80'
};