import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Stars, Text } from '@react-three/drei';
import { planetaryData, simulationSettings } from '../data/mock';
import * as THREE from 'three';

// Planet component
const Planet = ({ data, time, onClick, showLabels }) => {
  const meshRef = useRef();
  const orbitRef = useRef();
  
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y += data.rotationSpeed;
      
      if (data.orbitRadius && !data.parent) {
        const angle = time * data.orbitSpeed;
        meshRef.current.position.x = Math.cos(angle) * data.orbitRadius;
        meshRef.current.position.z = Math.sin(angle) * data.orbitRadius;
      } else if (data.parent) {
        // For moon orbiting Earth
        const earthAngle = time * planetaryData.earth.orbitSpeed;
        const earthX = Math.cos(earthAngle) * planetaryData.earth.orbitRadius;
        const earthZ = Math.sin(earthAngle) * planetaryData.earth.orbitRadius;
        
        const moonAngle = time * data.orbitSpeed;
        meshRef.current.position.x = earthX + Math.cos(moonAngle) * data.orbitRadius;
        meshRef.current.position.z = earthZ + Math.sin(moonAngle) * data.orbitRadius;
      }
    }
  });

  return (
    <group>
      <mesh
        ref={meshRef}
        position={data.position}
        onClick={() => onClick(data)}
        onPointerOver={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'pointer';
        }}
        onPointerOut={(e) => {
          e.stopPropagation();
          document.body.style.cursor = 'default';
        }}
      >
        <sphereGeometry args={[data.radius, 32, 32]} />
        <meshStandardMaterial
          color={data.color}
          emissive={data.emissive ? data.color : '#000000'}
          emissiveIntensity={data.emissive ? 0.3 : 0}
        />
      </mesh>
      
      {showLabels && (
        <Text
          position={[
            data.position[0],
            data.position[1] + data.radius + 2,
            data.position[2]
          ]}
          fontSize={1.5}
          color="white"
          anchorX="center"
          anchorY="middle"
        >
          {data.name}
        </Text>
      )}
    </group>
  );
};

// Orbit path component
const OrbitPath = ({ radius, visible }) => {
  const points = [];
  for (let i = 0; i <= 64; i++) {
    const angle = (i / 64) * Math.PI * 2;
    points.push(new THREE.Vector3(Math.cos(angle) * radius, 0, Math.sin(angle) * radius));
  }
  
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  
  return visible ? (
    <line geometry={geometry}>
      <lineBasicMaterial color="#444444" opacity={0.5} transparent />
    </line>
  ) : null;
};

// Main scene component
const SolarSystemScene = ({ onPlanetClick, settings }) => {
  const [time, setTime] = useState(0);
  
  useFrame(() => {
    setTime(prev => prev + settings.timeSpeed * 0.01);
  });

  return (
    <>
      <ambientLight intensity={settings.ambientLightIntensity} />
      <pointLight position={[0, 0, 0]} intensity={settings.pointLightIntensity} />
      
      <Stars radius={300} depth={60} count={20000} factor={7} />
      
      {/* Orbit paths */}
      {Object.values(planetaryData).map(planet => (
        planet.orbitRadius && !planet.parent ? (
          <OrbitPath key={`orbit-${planet.id}`} radius={planet.orbitRadius} visible={settings.showOrbits} />
        ) : null
      ))}
      
      {/* Moon orbit around Earth */}
      {settings.showOrbits && (
        <group>
          <OrbitPath radius={planetaryData.moon.orbitRadius} visible={settings.showOrbits} />
        </group>
      )}
      
      {/* Planets */}
      {Object.values(planetaryData).map(planet => (
        <Planet
          key={planet.id}
          data={planet}
          time={time}
          onClick={onPlanetClick}
          showLabels={settings.showLabels}
        />
      ))}
    </>
  );
};

const PlanetarySystem = () => {
  const [selectedPlanet, setSelectedPlanet] = useState(null);
  const [settings, setSettings] = useState(simulationSettings);

  const handlePlanetClick = (planet) => {
    setSelectedPlanet(planet);
  };

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  return (
    <div className="relative w-full h-screen bg-black overflow-hidden">
      {/* 3D Canvas */}
      <Canvas
        camera={{ position: [0, 20, settings.cameraDistance], fov: 60 }}
        style={{ background: 'radial-gradient(circle, #001122 0%, #000000 100%)' }}
      >
        <OrbitControls
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={20}
          maxDistance={200}
        />
        <SolarSystemScene onPlanetClick={handlePlanetClick} settings={settings} />
      </Canvas>

      {/* Control Panel */}
      <div className="absolute top-4 left-4 bg-black/80 backdrop-blur-sm border border-gray-600 rounded-lg p-4 text-white min-w-[300px]">
        <h2 className="text-xl font-bold mb-4 text-center">Solar System Controls</h2>
        
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm">Time Speed:</label>
            <input
              type="range"
              min="0"
              max="5"
              step="0.1"
              value={settings.timeSpeed}
              onChange={(e) => handleSettingChange('timeSpeed', parseFloat(e.target.value))}
              className="w-32"
            />
            <span className="text-sm w-8">{settings.timeSpeed.toFixed(1)}</span>
          </div>
          
          <div className="flex items-center justify-between">
            <label className="text-sm">Show Orbits:</label>
            <input
              type="checkbox"
              checked={settings.showOrbits}
              onChange={(e) => handleSettingChange('showOrbits', e.target.checked)}
              className="w-4 h-4"
            />
          </div>
          
          <div className="flex items-center justify-between">
            <label className="text-sm">Show Labels:</label>
            <input
              type="checkbox"
              checked={settings.showLabels}
              onChange={(e) => handleSettingChange('showLabels', e.target.checked)}
              className="w-4 h-4"
            />
          </div>
        </div>
      </div>

      {/* Planet Information Panel */}
      {selectedPlanet && (
        <div className="absolute top-4 right-4 bg-black/90 backdrop-blur-sm border border-gray-600 rounded-lg p-6 text-white max-w-[400px]">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-center flex-1">{selectedPlanet.name}</h3>
            <button
              onClick={() => setSelectedPlanet(null)}
              className="text-gray-400 hover:text-white text-xl ml-4"
            >
              ×
            </button>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-center mb-4">
              <div
                className="w-16 h-16 rounded-full border-2 border-white/20"
                style={{ backgroundColor: selectedPlanet.color }}
              />
            </div>
            
            <p className="text-gray-300 text-sm leading-relaxed">
              {selectedPlanet.description}
            </p>
            
            <div className="border-t border-gray-600 pt-4">
              <h4 className="text-lg font-semibold mb-2">Key Facts:</h4>
              <ul className="space-y-1 text-sm">
                {selectedPlanet.facts.map((fact, index) => (
                  <li key={index} className="text-gray-300">• {fact}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="absolute bottom-4 left-4 bg-black/80 backdrop-blur-sm border border-gray-600 rounded-lg p-4 text-white">
        <h4 className="font-semibold mb-2">Controls:</h4>
        <ul className="text-sm space-y-1 text-gray-300">
          <li>• Left click + drag to rotate view</li>
          <li>• Right click + drag to pan</li>
          <li>• Mouse wheel to zoom</li>
          <li>• Click on planets for information</li>
        </ul>
      </div>
    </div>
  );
};

export default PlanetarySystem;