"""
============================================================
CAMPUS360 - CONTEXT TELEMETRY SEED
============================================================

Seeds synthetic context telemetry used by the
Optimization & Decision Layer.

These values represent the hackathon/demo scenario:

    Actual Energy : 185 kWh
    Expected      : 50 kWh
    Occupancy     : 22 %
    Working Day   : YES
    Temperature   : 33 °C
    HVAC Load     : 90 %
    Hour          : 14 (2 PM)

The data is stored in the existing telemetry table.
No new database table is required.
============================================================
"""

from datetime import datetime

from sqlalchemy import delete, select

from backend.core.database import SessionLocal
from backend.models.building import Building
from backend.models.device import Device
from backend.models.telemetry import Telemetry


# ============================================================
# DEMO CONTEXT
# ============================================================

CONTEXT_DEVICES = [
    {
        "device_code": "CTX-ENERGY-ACTUAL",
        "name": "Context Energy Actual",
        "device_type": "CONTEXT_SENSOR",
        "category": "CONTEXT",
        "unit": "kWh",
        "metric": "energy_actual",
        "value": 185.0,
    },
    {
        "device_code": "CTX-ENERGY-EXPECTED",
        "name": "Context Energy Expected",
        "device_type": "CONTEXT_SENSOR",
        "category": "CONTEXT",
        "unit": "kWh",
        "metric": "energy_expected",
        "value": 50.0,
    },
    {
        "device_code": "CTX-OCCUPANCY",
        "name": "Context Occupancy",
        "device_type": "OCCUPANCY_SENSOR",
        "category": "CONTEXT",
        "unit": "%",
        "metric": "occupancy",
        "value": 22.0,
    },
    {
        "device_code": "CTX-TEMPERATURE",
        "name": "Context Temperature",
        "device_type": "TEMPERATURE_SENSOR",
        "category": "CONTEXT",
        "unit": "C",
        "metric": "temperature",
        "value": 33.0,
    },
    {
        "device_code": "CTX-HVAC",
        "name": "Context HVAC Load",
        "device_type": "HVAC_SENSOR",
        "category": "CONTEXT",
        "unit": "%",
        "metric": "hvac_load",
        "value": 90.0,
    },
    {
        "device_code": "CTX-WORKING-DAY",
        "name": "Context Working Day",
        "device_type": "SCHEDULE_SENSOR",
        "category": "CONTEXT",
        "unit": "boolean",
        "metric": "working_day",
        "value": 1.0,
    },
    {
        "device_code": "CTX-HOUR",
        "name": "Context Hour",
        "device_type": "SCHEDULE_SENSOR",
        "category": "CONTEXT",
        "unit": "hour",
        "metric": "hour",
        "value": 14.0,
    },
]


# ============================================================
# BUILDING SELECTION
# ============================================================

def get_target_building(db):
    """
    Select the Administration Building when available.

    Falls back to the first building so the seed script
    remains usable with the existing development database.
    """

    statement = (
        select(Building)
        .where(
            Building.name.ilike(
                "%Administration%"
            )
        )
        .order_by(
            Building.created_at.asc()
        )
    )

    building = db.scalar(statement)

    if building is not None:
        return building

    statement = (
        select(Building)
        .order_by(
            Building.created_at.asc()
        )
    )

    building = db.scalar(statement)

    if building is None:
        raise RuntimeError(
            "No buildings exist in the database. "
            "Create a building before running this seed script."
        )

    return building


# ============================================================
# DEVICE CREATION / REUSE
# ============================================================

def get_or_create_device(
    db,
    building_id,
    definition,
):
    """
    Reuse an existing context device or create it.
    """

    statement = (
        select(Device)
        .where(
            Device.device_code
            == definition["device_code"]
        )
    )

    device = db.scalar(statement)

    if device is not None:

        # Keep the device associated with the target
        # building used by this demo scenario.
        device.building_id = building_id

        return device

    device = Device(
        device_code=definition["device_code"],
        building_id=building_id,
        name=definition["name"],
        device_type=definition["device_type"],
        category=definition["category"],
        unit=definition["unit"],
        status="ACTIVE",
    )

    db.add(device)
    db.flush()

    return device


# ============================================================
# MAIN
# ============================================================

def seed_context_telemetry():

    db = SessionLocal()

    try:

        building = get_target_building(db)

        print(
            "\n============================================================"
        )

        print(
            "CAMPUS360 CONTEXT TELEMETRY SEED"
        )

        print(
            "============================================================"
        )

        print(
            "\nTarget building:"
        )

        print(
            building.name
        )

        print(
            "Building ID:"
        )

        print(
            building.id
        )

        timestamp = datetime.utcnow()

        devices = []

        # ----------------------------------------------------
        # Create / reuse context devices
        # ----------------------------------------------------

        for definition in CONTEXT_DEVICES:

            device = get_or_create_device(
                db,
                building.id,
                definition,
            )

            devices.append(
                (
                    device,
                    definition
                )
            )

        db.commit()

        # ----------------------------------------------------
        # Remove previous context telemetry
        #
        # Only telemetry belonging to our deterministic
        # context devices is removed.
        # ----------------------------------------------------

        device_ids = [
            device.id
            for device, _ in devices
        ]

        db.execute(
            delete(Telemetry).where(
                Telemetry.device_id.in_(
                    device_ids
                )
            )
        )

        # ----------------------------------------------------
        # Insert latest demo context
        # ----------------------------------------------------

        for device, definition in devices:

            telemetry = Telemetry(
                device_id=device.id,
                metric=definition["metric"],
                value=definition["value"],
                unit=definition["unit"],
                timestamp=timestamp,
            )

            db.add(telemetry)

        db.commit()

        print(
            "\nContext telemetry seeded successfully."
        )

        print(
            "\nDemo context:"
        )

        print(
            "  Actual energy : 185 kWh"
        )

        print(
            "  Expected      : 50 kWh"
        )

        print(
            "  Occupancy     : 22 %"
        )

        print(
            "  Working day   : YES"
        )

        print(
            "  Temperature   : 33 °C"
        )

        print(
            "  HVAC load     : 90 %"
        )

        print(
            "  Hour          : 14:00"
        )

        print(
            "\nThese values are now stored in the existing"
        )

        print(
            "telemetry table and can be consumed by the AI layer."
        )

        print(
            "\n============================================================"
        )

    except Exception:

        db.rollback()
        raise

    finally:

        db.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    seed_context_telemetry()