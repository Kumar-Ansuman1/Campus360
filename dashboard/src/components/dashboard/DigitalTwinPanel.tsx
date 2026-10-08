import { useEffect, useRef, useState } from "react"
import type { MutableRefObject } from "react"
import { Canvas, useFrame, useThree } from "@react-three/fiber"
import { Html, OrbitControls } from "@react-three/drei"
import * as THREE from "three"

import type { DigitalTwinState } from "../../types/dashboard"

type BuildingStatus =
  | "NORMAL"
  | "WARNING"
  | "ATTENTION"
  | "CRITICAL"

type Facility = {
  id: string
  name: string
  type: string
  status: BuildingStatus
  energy: number
  water: number
  occupancy: number
  position: [number, number, number]
  size: [number, number, number]
}

const facilities: Facility[] = [
  {
    id: "d040b2f2-9ea8-4336-a9f9-9c72b07e2597",
    name: "Administration Building",
    type: "OFFICE",
    status: "NORMAL",
    energy: 45.8,
    water: 138.7,
    occupancy: 72.5,
    position: [-5.2, 0, -3.5],
    size: [3.4, 4.8, 3],
  },
  {
    id: "static-2",
    name: "Office Tower B",
    type: "Corporate Office",
    status: "NORMAL",
    energy: 142,
    water: 9800,
    occupancy: 64,
    position: [5.2, 0, -3.5],
    size: [3.4, 5.2, 3],
  },
  {
    id: "static-3",
    name: "Auditorium",
    type: "Event Facility",
    status: "NORMAL",
    energy: 96,
    water: 6200,
    occupancy: 48,
    position: [-4.6, 0, 4],
    size: [4.2, 2.1, 3],
  },
  {
    id: "static-4",
    name: "Dining Block",
    type: "Food & Recreation",
    status: "WARNING",
    energy: 128,
    water: 7100,
    occupancy: 71,
    position: [4.6, 0, 4],
    size: [4.2, 2.3, 3],
  },
]

function getStatusColor(status: BuildingStatus) {
  switch (status) {
    case "NORMAL":
      return "#10b981"

    case "WARNING":
      return "#eab308"

    case "ATTENTION":
      return "#f59e0b"

    case "CRITICAL":
      return "#ef4444"
  }
}

function getStatusTextClass(status: BuildingStatus) {
  switch (status) {
    case "NORMAL":
      return "text-emerald-600"

    case "WARNING":
      return "text-yellow-600"

    case "ATTENTION":
      return "text-amber-600"

    case "CRITICAL":
      return "text-red-600"
  }
}

function getPriorityStyles(priority: string) {
  const value = priority.toUpperCase()

  if (value.startsWith("P1")) {
    return {
      badge: "bg-red-50 text-red-700 border-red-100",
      dot: "bg-red-500",
    }
  }

  if (value.startsWith("P2")) {
    return {
      badge: "bg-orange-50 text-orange-700 border-orange-100",
      dot: "bg-orange-500",
    }
  }

  if (value.startsWith("P3")) {
    return {
      badge: "bg-yellow-50 text-yellow-700 border-yellow-100",
      dot: "bg-yellow-500",
    }
  }

  return {
    badge: "bg-slate-50 text-slate-600 border-slate-200",
    dot: "bg-slate-400",
  }
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 1,
  }).format(value)
}

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-IN", {
    maximumFractionDigits: 0,
  }).format(value)
}

/* -------------------------------------------------------------------------- */
/* Camera Focus Controller                                                    */
/* -------------------------------------------------------------------------- */

function CameraFocusController({
  selectedBuilding,
  controlsRef,
}: {
  selectedBuilding: string
  controlsRef: MutableRefObject<any>
}) {
  const { camera } = useThree()

  const isAnimating = useRef(true)

  const desiredPosition = useRef(
    new THREE.Vector3(15, 13, 17),
  )

  const desiredTarget = useRef(
    new THREE.Vector3(0, 1.5, 0),
  )

  useEffect(() => {
    const facility = facilities.find(
      (item) => item.id === selectedBuilding,
    )

    if (!facility) {
      return
    }

    const [x, , z] = facility.position

    desiredPosition.current.set(
      x + 8,
      7,
      z + 9,
    )

    desiredTarget.current.set(
      x,
      Math.max(facility.size[1] * 0.35, 1.5),
      z,
    )

    isAnimating.current = true
  }, [
    selectedBuilding,
    camera,
    controlsRef,
  ])

  useFrame((_, delta) => {
    if (!isAnimating.current) {
      return
    }

    const speed = Math.min(
      delta * 3.5,
      1,
    )

    camera.position.lerp(
      desiredPosition.current,
      speed,
    )

    if (controlsRef.current) {
      controlsRef.current.target.lerp(
        desiredTarget.current,
        speed,
      )

      controlsRef.current.update()
    }

    const cameraDistance =
      camera.position.distanceTo(
        desiredPosition.current,
      )

    const targetDistance =
      controlsRef.current
        ? controlsRef.current.target.distanceTo(
            desiredTarget.current,
          )
        : 0

    if (
      cameraDistance < 0.05 &&
      targetDistance < 0.05
    ) {
      camera.position.copy(
        desiredPosition.current,
      )

      if (controlsRef.current) {
        controlsRef.current.target.copy(
          desiredTarget.current,
        )

        controlsRef.current.update()
      }

      isAnimating.current = false
    }
  })

  return null
}

/* -------------------------------------------------------------------------- */
/* Campus Ground                                                              */
/* -------------------------------------------------------------------------- */

function CampusGround() {
  return (
    <group>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.2, 0]}
        receiveShadow
      >
        <planeGeometry args={[18, 14]} />

        <meshStandardMaterial
          color="#dbeafe"
          roughness={0.9}
        />
      </mesh>

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.08, 0]}
        receiveShadow
      >
        <circleGeometry args={[3.2, 48]} />

        <meshStandardMaterial
          color="#f8fafc"
          roughness={0.8}
        />
      </mesh>

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.12, 0]}
      >
        <planeGeometry args={[18, 1.7]} />

        <meshStandardMaterial
          color="#94a3b8"
          roughness={0.9}
        />
      </mesh>

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.11, 0]}
      >
        <planeGeometry args={[1.7, 14]} />

        <meshStandardMaterial
          color="#94a3b8"
          roughness={0.9}
        />
      </mesh>

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.095, 0]}
      >
        <planeGeometry args={[18, 0.05]} />

        <meshStandardMaterial color="#f8fafc" />
      </mesh>

      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, -0.09, 0]}
      >
        <planeGeometry args={[0.05, 14]} />

        <meshStandardMaterial color="#f8fafc" />
      </mesh>
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Facility Building                                                          */
/* -------------------------------------------------------------------------- */

function FacilityBuilding({
  facility,
  selected,
  onSelect,
  digitalTwin,
}: {
  facility: Facility
  selected: boolean
  onSelect: () => void
  digitalTwin: DigitalTwinState
}) {
  const [width, height, depth] = facility.size

  const isLiveBuilding =
    facility.id === digitalTwin.building_id

  const liveStatus = isLiveBuilding
    ? digitalTwin.status
    : facility.status

  const liveName = isLiveBuilding
    ? digitalTwin.building
    : facility.name

  const statusColor =
    getStatusColor(liveStatus)

  return (
    <group
      position={facility.position}
      onClick={(event) => {
        event.stopPropagation()
        onSelect()
      }}
    >
      <mesh
        position={[0, 0.12, 0]}
        receiveShadow
      >
        <boxGeometry
          args={[
            width + 0.3,
            0.25,
            depth + 0.3,
          ]}
        />

        <meshStandardMaterial
          color="#64748b"
          roughness={0.8}
        />
      </mesh>

      <mesh
        position={[0, height / 2, 0]}
        castShadow
        receiveShadow
      >
        <boxGeometry
          args={[
            width,
            height,
            depth,
          ]}
        />

        <meshStandardMaterial
          color="#f8fafc"
          roughness={0.55}
          metalness={0.05}
        />
      </mesh>

      <mesh
        position={[0, height + 0.12, 0]}
        castShadow
      >
        <boxGeometry
          args={[
            width + 0.12,
            0.25,
            depth + 0.12,
          ]}
        />

        <meshStandardMaterial
          color={statusColor}
          roughness={0.4}
          emissive={statusColor}
          emissiveIntensity={
            selected ? 0.3 : 0.08
          }
        />
      </mesh>

      <BuildingWindows
        width={width}
        height={height}
        depth={depth}
      />

      <mesh
        position={[
          0,
          Math.min(height * 0.2, 0.8),
          depth / 2 + 0.05,
        ]}
      >
        <boxGeometry
          args={[0.7, 0.9, 0.08]}
        />

        <meshStandardMaterial
          color="#1e293b"
          roughness={0.3}
          metalness={0.2}
        />
      </mesh>

      <Html
        position={[0, height + 0.7, 0]}
        center
        distanceFactor={8}
        zIndexRange={[10, 0]}
      >
        <div
          className={`pointer-events-none rounded-lg border bg-white px-2.5 py-1.5 shadow-md ${
            selected
              ? "border-blue-300"
              : "border-slate-200"
          }`}
        >
          <div className="flex items-center gap-1.5">
            <span
              className="h-2 w-2 rounded-full"
              style={{
                backgroundColor: statusColor,
              }}
            />

            <span className="whitespace-nowrap text-[10px] font-semibold text-slate-700">
              {liveName}
            </span>
          </div>
        </div>
      </Html>

      {selected && (
        <mesh
          position={[
            0,
            height + 0.4,
            0,
          ]}
        >
          <sphereGeometry
            args={[0.15, 20, 20]}
          />

          <meshStandardMaterial
            color="#2563eb"
            emissive="#2563eb"
            emissiveIntensity={1}
          />
        </mesh>
      )}
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Windows                                                                    */
/* -------------------------------------------------------------------------- */

function BuildingWindows({
  width,
  height,
  depth,
}: {
  width: number
  height: number
  depth: number
}) {
  const windowRows = Math.max(
    1,
    Math.floor(height / 1.1),
  )

  const windowColumns = Math.max(
    2,
    Math.floor(width / 0.8),
  )

  const windows = []

  for (
    let row = 0;
    row < windowRows;
    row++
  ) {
    for (
      let column = 0;
      column < windowColumns;
      column++
    ) {
      const x =
        -width / 2 +
        0.55 +
        column *
          ((width - 1.1) /
            Math.max(
              windowColumns - 1,
              1,
            ))

      const y =
        0.8 +
        row *
          ((height - 1.3) /
            Math.max(
              windowRows - 1,
              1,
            ))

      windows.push(
        <mesh
          key={`${row}-${column}`}
          position={[
            x,
            y,
            depth / 2 + 0.025,
          ]}
        >
          <boxGeometry
            args={[0.38, 0.42, 0.05]}
          />

          <meshStandardMaterial
            color="#60a5fa"
            roughness={0.25}
            metalness={0.25}
          />
        </mesh>,
      )
    }
  }

  return <>{windows}</>
}

/* -------------------------------------------------------------------------- */
/* Water Tank                                                                 */
/* -------------------------------------------------------------------------- */

function WaterTank({
  position,
  label,
}: {
  position: [number, number, number]
  label: string
}) {
  return (
    <group position={position}>
      <mesh
        position={[-0.45, 0.7, 0]}
        castShadow
      >
        <cylinderGeometry
          args={[0.08, 0.08, 1.4, 8]}
        />

        <meshStandardMaterial
          color="#64748b"
        />
      </mesh>

      <mesh
        position={[0.45, 0.7, 0]}
        castShadow
      >
        <cylinderGeometry
          args={[0.08, 0.08, 1.4, 8]}
        />

        <meshStandardMaterial
          color="#64748b"
        />
      </mesh>

      <mesh
        position={[0, 1.55, 0]}
        castShadow
      >
        <cylinderGeometry
          args={[0.75, 0.75, 1.25, 32]}
        />

        <meshStandardMaterial
          color="#60a5fa"
          roughness={0.3}
          metalness={0.15}
        />
      </mesh>

      <mesh
        position={[0, 2.2, 0]}
        castShadow
      >
        <sphereGeometry
          args={[
            0.75,
            32,
            16,
            0,
            Math.PI * 2,
            0,
            Math.PI / 2,
          ]}
        />

        <meshStandardMaterial
          color="#93c5fd"
          roughness={0.25}
          metalness={0.15}
        />
      </mesh>

      <Html
        position={[0, 2.8, 0]}
        center
        distanceFactor={9}
      >
        <div className="pointer-events-none rounded-md border border-blue-100 bg-white px-2 py-1 text-[9px] font-semibold text-blue-600 shadow-sm">
          💧 {label}
        </div>
      </Html>
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Car                                                                        */
/* -------------------------------------------------------------------------- */

function Car({
  position,
  rotation = 0,
  color = "#2563eb",
}: {
  position: [number, number, number]
  rotation?: number
  color?: string
}) {
  return (
    <group
      position={position}
      rotation={[0, rotation, 0]}
    >
      <mesh
        position={[0, 0.25, 0]}
        castShadow
      >
        <boxGeometry
          args={[0.65, 0.3, 1.15]}
        />

        <meshStandardMaterial
          color={color}
          roughness={0.45}
        />
      </mesh>

      <mesh
        position={[0, 0.48, -0.05]}
        castShadow
      >
        <boxGeometry
          args={[0.5, 0.28, 0.55]}
        />

        <meshStandardMaterial
          color="#bfdbfe"
          roughness={0.25}
          metalness={0.15}
        />
      </mesh>

      <Wheel
        position={[-0.34, 0.12, -0.38]}
      />

      <Wheel
        position={[0.34, 0.12, -0.38]}
      />

      <Wheel
        position={[-0.34, 0.12, 0.38]}
      />

      <Wheel
        position={[0.34, 0.12, 0.38]}
      />
    </group>
  )
}

function Wheel({
  position,
}: {
  position: [number, number, number]
}) {
  return (
    <mesh
      position={position}
      rotation={[Math.PI / 2, 0, 0]}
    >
      <cylinderGeometry
        args={[0.1, 0.1, 0.08, 12]}
      />

      <meshStandardMaterial
        color="#1e293b"
        roughness={0.8}
      />
    </mesh>
  )
}

/* -------------------------------------------------------------------------- */
/* Parking Area                                                               */
/* -------------------------------------------------------------------------- */

function ParkingArea({
  parking,
}: {
  parking: number
}) {
  const cars: [number, number, number][] = [
    [-6.5, 0, 2.7],
    [-5.7, 0, 2.7],
    [-4.9, 0, 2.7],
    [-4.1, 0, 2.7],
    [-3.3, 0, 2.7],
    [-2.5, 0, 2.7],
    [-6.5, 0, 3.65],
    [-5.7, 0, 3.65],
    [-4.9, 0, 3.65],
    [-4.1, 0, 3.65],
    [-3.3, 0, 3.65],
    [-2.5, 0, 3.65],
  ]

  const carColors = [
    "#2563eb",
    "#64748b",
    "#ef4444",
    "#10b981",
    "#f59e0b",
    "#334155",
  ]

  return (
    <group>
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[-4.5, -0.09, 3.2]}
        receiveShadow
      >
        <planeGeometry
          args={[5.5, 2.6]}
        />

        <meshStandardMaterial
          color="#64748b"
          roughness={0.9}
        />
      </mesh>

      {Array.from({ length: 7 }).map(
        (_, index) => (
          <mesh
            key={index}
            rotation={[
              -Math.PI / 2,
              0,
              0,
            ]}
            position={[
              -6.85 +
                index * 0.8,
              -0.07,
              3.2,
            ]}
          >
            <planeGeometry
              args={[0.03, 2.3]}
            />

            <meshStandardMaterial
              color="#f8fafc"
            />
          </mesh>
        ),
      )}

      {cars.map(
        (position, index) => (
          <Car
            key={index}
            position={position}
            rotation={Math.PI / 2}
            color={
              carColors[
                index %
                  carColors.length
              ]
            }
          />
        ),
      )}

      <Html
        position={[
          -4.5,
          0.2,
          4.7,
        ]}
        center
        distanceFactor={9}
      >
        <div className="pointer-events-none rounded-md border border-slate-200 bg-white px-2 py-1 text-[9px] font-semibold text-slate-600 shadow-sm">
          🅿️ Parking • {parking}%
        </div>
      </Html>
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Road Vehicles                                                              */
/* -------------------------------------------------------------------------- */

function RoadVehicles() {
  return (
    <group>
      <Car
        position={[-2.8, 0, -0.45]}
        rotation={Math.PI / 2}
        color="#2563eb"
      />

      <Car
        position={[2.6, 0, 0.45]}
        rotation={-Math.PI / 2}
        color="#ef4444"
      />

      <Car
        position={[0.45, 0, -2.8]}
        rotation={0}
        color="#10b981"
      />

      <Car
        position={[-0.45, 0, 2.4]}
        rotation={Math.PI}
        color="#64748b"
      />
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Trees                                                                      */
/* -------------------------------------------------------------------------- */

function Tree({
  position,
  scale = 1,
}: {
  position: [number, number, number]
  scale?: number
}) {
  return (
    <group
      position={position}
      scale={scale}
    >
      <mesh
        position={[0, 0.45, 0]}
        castShadow
      >
        <cylinderGeometry
          args={[0.12, 0.16, 0.9, 8]}
        />

        <meshStandardMaterial
          color="#78350f"
          roughness={0.9}
        />
      </mesh>

      <mesh
        position={[0, 1.15, 0]}
        castShadow
      >
        <sphereGeometry
          args={[0.6, 16, 16]}
        />

        <meshStandardMaterial
          color="#16a34a"
          roughness={0.9}
        />
      </mesh>

      <mesh
        position={[0, 1.55, 0]}
        castShadow
      >
        <sphereGeometry
          args={[0.45, 16, 16]}
        />

        <meshStandardMaterial
          color="#22c55e"
          roughness={0.9}
        />
      </mesh>
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Campus Entrance                                                            */
/* -------------------------------------------------------------------------- */

function CampusEntrance() {
  return (
    <group position={[0, 0, 6.2]}>
      <mesh
        position={[0, 0.1, 0]}
        receiveShadow
      >
        <boxGeometry
          args={[4, 0.2, 1]}
        />

        <meshStandardMaterial
          color="#cbd5e1"
        />
      </mesh>

      <mesh
        position={[-1.5, 1.4, 0]}
        castShadow
      >
        <boxGeometry
          args={[0.3, 2.8, 0.3]}
        />

        <meshStandardMaterial
          color="#2563eb"
        />
      </mesh>

      <mesh
        position={[1.5, 1.4, 0]}
        castShadow
      >
        <boxGeometry
          args={[0.3, 2.8, 0.3]}
        />

        <meshStandardMaterial
          color="#2563eb"
        />
      </mesh>

      <mesh
        position={[0, 2.7, 0]}
        castShadow
      >
        <boxGeometry
          args={[3.3, 0.35, 0.4]}
        />

        <meshStandardMaterial
          color="#2563eb"
        />
      </mesh>

      <Html
        position={[0, 2.95, 0]}
        center
        distanceFactor={9}
      >
        <div className="pointer-events-none whitespace-nowrap rounded-md bg-white px-2 py-1 text-[9px] font-semibold text-blue-600 shadow-sm">
          CAMPUS360
        </div>
      </Html>
    </group>
  )
}

/* -------------------------------------------------------------------------- */
/* Campus Scene                                                               */
/* -------------------------------------------------------------------------- */

function CampusScene({
  selectedBuilding,
  onSelectBuilding,
  digitalTwin,
}: {
  selectedBuilding: string
  onSelectBuilding: (id: string) => void
  digitalTwin: DigitalTwinState
}) {
  return (
    <>
      <color
        attach="background"
        args={["#dff3ff"]}
      />

      <ambientLight intensity={1.8} />

      <directionalLight
        position={[8, 14, 10]}
        intensity={3}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />

      <directionalLight
        position={[-8, 8, -6]}
        intensity={1.2}
      />

      <CampusGround />

      {facilities.map(
        (facility) => (
          <FacilityBuilding
            key={facility.id}
            facility={facility}
            selected={
              selectedBuilding ===
              facility.id
            }
            onSelect={() =>
              onSelectBuilding(
                facility.id,
              )
            }
            digitalTwin={digitalTwin}
          />
        ),
      )}

      <WaterTank
        position={[7, 0, 3.8]}
        label="Water Tank A"
      />

      <WaterTank
        position={[7, 0, -0.8]}
        label="Water Tank B"
      />

      <ParkingArea
        parking={digitalTwin.parking}
      />

      <RoadVehicles />

      <CampusEntrance />

      <Tree
        position={[-7, 0, -5.5]}
        scale={1.1}
      />

      <Tree
        position={[7, 0, -5.5]}
        scale={1.1}
      />

      <Tree
        position={[-7, 0, 5.2]}
      />

      <Tree
        position={[7, 0, 5.2]}
      />

      <Tree
        position={[-1.9, 0, 5.1]}
        scale={0.8}
      />

      <Tree
        position={[1.9, 0, -5.1]}
        scale={0.8}
      />

      <Tree
        position={[7, 0, 0]}
        scale={0.75}
      />

      <Tree
        position={[-7, 0, 0]}
        scale={0.75}
      />
    </>
  )
}

/* -------------------------------------------------------------------------- */
/* Main Panel                                                                 */
/* -------------------------------------------------------------------------- */

type DigitalTwinPanelProps = {
  digitalTwin: DigitalTwinState
}

function DigitalTwinPanel({
  digitalTwin,
}: DigitalTwinPanelProps) {
  const [
    selectedBuildingId,
    setSelectedBuildingId,
  ] = useState(
    digitalTwin.building_id,
  )

  useEffect(() => {
    setSelectedBuildingId(
      digitalTwin.building_id,
    )
  }, [digitalTwin.building_id])

  const controlsRef =
    useRef<any>(null)

  const selectedFacility =
    facilities.find(
      (facility) =>
        facility.id ===
        selectedBuildingId,
    ) ?? facilities[0]

  const isLiveBuilding =
    selectedFacility.id ===
    digitalTwin.building_id

  const selectedName = isLiveBuilding
    ? digitalTwin.building
    : selectedFacility.name

  const selectedType = isLiveBuilding
    ? digitalTwin.building_type
    : selectedFacility.type

  const selectedStatus = isLiveBuilding
    ? digitalTwin.status
    : selectedFacility.status

  const selectedEnergy = isLiveBuilding
    ? digitalTwin.energy
    : selectedFacility.energy

  const selectedWater = isLiveBuilding
    ? digitalTwin.water
    : selectedFacility.water

  const selectedParking = isLiveBuilding
    ? digitalTwin.parking
    : selectedFacility.occupancy

  const optimization =
    isLiveBuilding
      ? digitalTwin.optimization
      : undefined

  const topPriority =
    optimization?.top_priority

  return (
    <section className="h-full rounded-2xl border border-blue-100 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Digital Twin
          </h2>

          <p className="text-sm text-slate-500">
            Interactive 3D representation of the campus
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-1.5">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />

          <span className="text-xs font-semibold text-blue-600">
            Live State
          </span>
        </div>
      </div>

      {/* 3D Scene */}
      <div className="relative mt-5 overflow-hidden rounded-xl border border-blue-100 bg-sky-50">
        <div className="h-96 w-full">
          <Canvas
            shadows
            camera={{
              position: [15, 13, 17],
              fov: 42,
            }}
          >
            <CampusScene
              selectedBuilding={
                selectedBuildingId
              }
              onSelectBuilding={
                setSelectedBuildingId
              }
              digitalTwin={digitalTwin}
            />

            <OrbitControls
              ref={controlsRef}
              makeDefault
              enableDamping
              dampingFactor={0.08}
              minDistance={10}
              maxDistance={28}
              minPolarAngle={0.45}
              maxPolarAngle={1.35}
              target={[0, 1.5, 0]}
            />

            <CameraFocusController
              selectedBuilding={
                selectedBuildingId
              }
              controlsRef={
                controlsRef
              }
            />
          </Canvas>
        </div>

        <div className="absolute left-3 top-3 rounded-lg border border-white bg-white/90 px-3 py-2 shadow-sm backdrop-blur">
          <p className="text-[10px] font-semibold text-slate-700">
            CAMPUS DIGITAL TWIN
          </p>

          <p className="mt-0.5 text-[9px] text-slate-400">
            Drag to rotate • Scroll to zoom • Click a facility
          </p>
        </div>

        <div className="absolute bottom-3 left-3 rounded-lg border border-white bg-white/90 px-3 py-2 shadow-sm backdrop-blur">
          <div className="flex items-center gap-3">
            <span className="text-[9px] text-slate-500">
              💧 2 Tanks
            </span>

            <span className="text-[9px] text-slate-500">
              🅿️ {digitalTwin.parking}%
            </span>

            <span className="text-[9px] text-slate-500">
              🚗 {digitalTwin.vehicles} Vehicles
            </span>
          </div>
        </div>

        <div className="absolute bottom-3 right-3 rounded-lg border border-white bg-white/90 px-3 py-2 shadow-sm backdrop-blur">
          <div className="flex flex-wrap items-center gap-3">
            <LegendItem
              color="bg-emerald-500"
              label="Normal"
            />

            <LegendItem
              color="bg-yellow-500"
              label="Warning"
            />

            <LegendItem
              color="bg-amber-500"
              label="Attention"
            />

            <LegendItem
              color="bg-red-500"
              label="Critical"
            />
          </div>
        </div>
      </div>

      {/* Selected Facility */}
      <div className="mt-4 rounded-xl border border-blue-100 bg-slate-50 p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-slate-400">
              Selected Facility
            </p>

            <h3 className="mt-1 text-sm font-semibold text-slate-900">
              {selectedName}
            </h3>

            <p className="mt-0.5 text-xs text-slate-400">
              {selectedType}
            </p>
          </div>

          <div className="flex items-center gap-2">
            <span
              className="h-2.5 w-2.5 rounded-full"
              style={{
                backgroundColor:
                  getStatusColor(
                    selectedStatus,
                  ),
              }}
            />

            <span
              className={`text-xs font-semibold ${getStatusTextClass(
                selectedStatus,
              )}`}
            >
              {selectedStatus}
            </span>
          </div>
        </div>

        {/* Live metrics */}
        <div className="mt-4 grid grid-cols-3 gap-3">
          <Metric
            label="Energy"
            value={`${selectedEnergy} kWh`}
          />

          <Metric
            label="Water"
            value={`${selectedWater.toLocaleString()} L`}
          />

          <Metric
            label={
              isLiveBuilding
                ? "Parking"
                : "Occupancy"
            }
            value={`${selectedParking}%`}
          />
        </div>

        {/* Backend Digital Twin values */}
        {isLiveBuilding && (
          <>
            <div className="mt-3 grid grid-cols-2 gap-3">
              <Metric
                label="Forecast"
                value={digitalTwin.forecast}
              />

              <Metric
                label="Priority"
                value={digitalTwin.priority}
              />
            </div>

            {/* AI Decision */}
            {topPriority && (
              <div className="mt-4 rounded-xl border border-red-100 bg-white p-4">
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-[10px] font-bold uppercase tracking-[0.12em] text-blue-500">
                      AI Decision
                    </p>

                    <div className="mt-1 flex items-center gap-2">
                      <span className="text-sm font-bold text-slate-900">
                        {topPriority.category}
                      </span>

                      <span
                        className={`inline-flex items-center gap-1.5 rounded-full border px-2 py-1 text-[10px] font-bold ${
                          getPriorityStyles(
                            topPriority.priority,
                          ).badge
                        }`}
                      >
                        <span
                          className={`h-1.5 w-1.5 rounded-full ${
                            getPriorityStyles(
                              topPriority.priority,
                            ).dot
                          }`}
                        />

                        {topPriority.priority}
                      </span>
                    </div>
                  </div>

                  <span className="rounded-full border border-red-100 bg-red-50 px-2.5 py-1 text-[10px] font-bold text-red-700">
                    {topPriority.status}
                  </span>
                </div>

                <div className="mt-3 rounded-lg bg-slate-50 p-3">
                  <p className="text-[10px] font-bold uppercase tracking-wide text-slate-400">
                    Recommended action
                  </p>

                  <p className="mt-1 text-xs font-semibold leading-5 text-slate-800">
                    {topPriority.recommended_action}
                  </p>
                </div>

                <div className="mt-3 grid grid-cols-3 gap-2">
                  <div className="rounded-lg border border-blue-100 bg-blue-50/50 p-2">
                    <p className="text-[9px] text-slate-400">
                      Energy saved
                    </p>

                    <p className="mt-1 text-xs font-bold text-slate-800">
                      {formatNumber(
                        topPriority.impact
                          .energy_saved_kwh_per_day,
                      )}
                    </p>

                    <p className="text-[9px] text-slate-400">
                      kWh/day
                    </p>
                  </div>

                  <div className="rounded-lg border border-blue-100 bg-blue-50/50 p-2">
                    <p className="text-[9px] text-slate-400">
                      Cost saving
                    </p>

                    <p className="mt-1 text-xs font-bold text-slate-800">
                      ₹
                      {formatCurrency(
                        topPriority.impact
                          .cost_saving_inr_per_day,
                      )}
                    </p>

                    <p className="text-[9px] text-slate-400">
                      per day
                    </p>
                  </div>

                  <div className="rounded-lg border border-blue-100 bg-blue-50/50 p-2">
                    <p className="text-[9px] text-slate-400">
                      CO₂ reduction
                    </p>

                    <p className="mt-1 text-xs font-bold text-slate-800">
                      {formatNumber(
                        topPriority.impact
                          .co2_reduction_kg_per_day,
                      )}
                    </p>

                    <p className="text-[9px] text-slate-400">
                      kg/day
                    </p>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}

/* -------------------------------------------------------------------------- */
/* UI Components                                                              */
/* -------------------------------------------------------------------------- */

function LegendItem({
  color,
  label,
}: {
  color: string
  label: string
}) {
  return (
    <div className="flex items-center gap-1.5">
      <span
        className={`h-2 w-2 rounded-full ${color}`}
      />

      <span className="text-[9px] text-slate-500">
        {label}
      </span>
    </div>
  )
}

function Metric({
  label,
  value,
}: {
  label: string
  value: string
}) {
  return (
    <div>
      <p className="text-[11px] text-slate-400">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-800">
        {value}
      </p>
    </div>
  )
}

export default DigitalTwinPanel