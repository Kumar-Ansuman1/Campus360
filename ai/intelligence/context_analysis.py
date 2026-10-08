"""
=================================================================
CAMPUS360 - ENERGY CONTEXT ANALYSIS
Optimization & Decision Layer

Purpose:
    Add contextual intelligence around energy consumption.

This module does NOT replace:
    - Anomaly detection
    - Forecasting
    - RAG
    - Decision reasoning
    - Recommendation engine
    - What-If simulation

It provides:
    - Actual energy
    - Expected energy
    - Deviation percentage
    - Occupancy
    - Working-day context
    - Temperature
    - HVAC load
    - Time
    - Context-aware energy status
    - Human-readable interpretation
=================================================================
"""


class EnergyContextAnalyzer:

    # ============================================================
    # CONFIGURATION
    # ============================================================

    DEFAULT_EXPECTED_ENERGY = 50.0

    DEFAULT_OCCUPANCY = 22.0

    DEFAULT_WORKING_DAY = True

    DEFAULT_TEMPERATURE = 33.0

    DEFAULT_HVAC_LOAD = 90.0

    DEFAULT_HOUR = 14

    # Context-aware thresholds.
    #
    # deviation <= 25%  -> NORMAL
    # deviation > 25%   -> HIGH
    # deviation > 50%   -> CRITICAL
    #
    # MODERATE is used for smaller positive deviations
    # when the deviation is above normal but not yet HIGH.
    NORMAL_THRESHOLD = 25.0
    HIGH_THRESHOLD = 50.0

    # ============================================================
    # SAFE NUMBER
    # ============================================================

    @staticmethod
    def _number(value, default=0.0):
        """
        Safely convert a value to float.
        """

        try:

            if value is None:
                return default

            return float(value)

        except (TypeError, ValueError):

            return default

    # ============================================================
    # CLAMP
    # ============================================================

    @staticmethod
    def _clamp(value, minimum, maximum):
        """
        Keep a numeric value inside a configured range.
        """

        return max(
            minimum,
            min(
                maximum,
                value
            )
        )

    # ============================================================
    # DEVIATION
    # ============================================================

    @classmethod
    def calculate_deviation(
        cls,
        actual_energy,
        expected_energy
    ):
        """
        Calculate percentage deviation from expected energy.

        Example:

            actual   = 185
            expected = 50

            deviation =
                ((185 - 50) / 50) * 100

            = 270%
        """

        actual = cls._number(
            actual_energy
        )

        expected = cls._number(
            expected_energy
        )

        if expected <= 0:
            return 0.0

        deviation = (
            (
                actual - expected
            )
            / expected
        ) * 100.0

        return round(
            deviation,
            2
        )

    # ============================================================
    # STATUS
    # ============================================================

    @classmethod
    def determine_status(
        cls,
        deviation_percent
    ):
        """
        Determine context-aware energy status.

        Rules:

            deviation <= 25%
                NORMAL

            25% < deviation <= 50%
                MODERATE

            deviation > 50%
                HIGH

            Critical is reserved for severe contextual
            conditions, such as very large deviation combined
            with low occupancy and high HVAC demand.
        """

        deviation = cls._number(
            deviation_percent
        )

        if deviation <= cls.NORMAL_THRESHOLD:
            return "NORMAL"

        if deviation <= cls.HIGH_THRESHOLD:
            return "MODERATE"

        return "HIGH"

    # ============================================================
    # CONTEXTUAL CRITICAL CHECK
    # ============================================================

    @classmethod
    def determine_context_status(
        cls,
        deviation_percent,
        occupancy,
        temperature,
        hvac_load
    ):
        """
        Determine the final context-aware status.

        A very large energy deviation can become CRITICAL
        when the surrounding context suggests that the
        consumption is difficult to justify.

        Example:

            deviation = 270%
            occupancy = 22%
            temperature = 33 C
            HVAC      = 90%

        Result:

            CRITICAL
        """

        deviation = cls._number(
            deviation_percent
        )

        occupancy = cls._clamp(
            cls._number(
                occupancy
            ),
            0.0,
            100.0
        )

        temperature = cls._number(
            temperature
        )

        hvac_load = cls._clamp(
            cls._number(
                hvac_load
            ),
            0.0,
            100.0
        )

        # Severe energy deviation.
        severe_deviation = (
            deviation > 50.0
        )

        # Low occupancy means high energy usage is
        # harder to justify.
        low_occupancy = (
            occupancy < 30.0
        )

        # High HVAC load can explain some consumption,
        # but becomes an important optimization signal
        # when occupancy is low.
        high_hvac = (
            hvac_load >= 80.0
        )

        # Hot environment increases HVAC demand.
        high_temperature = (
            temperature >= 30.0
        )

        if (
            severe_deviation
            and low_occupancy
            and high_hvac
        ):
            return "CRITICAL"

        if severe_deviation:
            return "HIGH"

        if (
            deviation > 25.0
            and low_occupancy
            and high_hvac
            and high_temperature
        ):
            return "HIGH"

        if deviation > 25.0:
            return "MODERATE"

        return "NORMAL"

    # ============================================================
    # INTERPRETATION
    # ============================================================

    @classmethod
    def build_interpretation(
        cls,
        actual_energy,
        expected_energy,
        deviation_percent,
        status,
        occupancy,
        working_day,
        temperature,
        hvac_load,
        hour
    ):
        """
        Generate a concise explanation that an administrator
        can understand.
        """

        actual = cls._number(
            actual_energy
        )

        expected = cls._number(
            expected_energy
        )

        occupancy = cls._clamp(
            cls._number(
                occupancy
            ),
            0.0,
            100.0
        )

        temperature = cls._number(
            temperature
        )

        hvac_load = cls._clamp(
            cls._number(
                hvac_load
            ),
            0.0,
            100.0
        )

        working_day_text = (
            "working day"
            if working_day
            else "non-working day"
        )

        hour_text = (
            f"{int(hour):02d}:00"
        )

        if status == "CRITICAL":

            return (
                f"Energy consumption is critically high: "
                f"{actual:.1f} kWh versus an expected "
                f"{expected:.1f} kWh "
                f"({deviation_percent:.1f}% above expected). "
                f"Occupancy is only {occupancy:.0f}% on a "
                f"{working_day_text}, while temperature is "
                f"{temperature:.1f}°C and HVAC load is "
                f"{hvac_load:.0f}%. "
                f"The high HVAC load relative to occupancy "
                f"is a strong optimization signal."
            )

        if status == "HIGH":

            return (
                f"Energy consumption is significantly above "
                f"expected levels by {deviation_percent:.1f}%. "
                f"Current occupancy is {occupancy:.0f}% and "
                f"HVAC load is {hvac_load:.0f}%."
            )

        if status == "MODERATE":

            return (
                f"Energy consumption is moderately above "
                f"expected levels by {deviation_percent:.1f}%. "
                f"Current operating context: "
                f"{occupancy:.0f}% occupancy, "
                f"{temperature:.1f}°C temperature, and "
                f"{hvac_load:.0f}% HVAC load."
            )

        return (
            f"Energy consumption is within the expected "
            f"operating range at {actual:.1f} kWh. "
            f"Current context is {occupancy:.0f}% occupancy "
            f"at {hour_text}."
        )

    # ============================================================
    # CONTEXT FLAGS
    # ============================================================

    @classmethod
    def build_flags(
        cls,
        occupancy,
        working_day,
        temperature,
        hvac_load,
        deviation_percent
    ):
        """
        Produce machine-readable contextual signals.

        These flags will later help the optimization engine
        explain WHY energy received a high priority.
        """

        occupancy = cls._clamp(
            cls._number(
                occupancy
            ),
            0.0,
            100.0
        )

        temperature = cls._number(
            temperature
        )

        hvac_load = cls._clamp(
            cls._number(
                hvac_load
            ),
            0.0,
            100.0
        )

        deviation = cls._number(
            deviation_percent
        )

        return {

            "low_occupancy":
                occupancy < 30.0,

            "high_temperature":
                temperature >= 30.0,

            "high_hvac_load":
                hvac_load >= 80.0,

            "large_energy_deviation":
                deviation > 50.0,

            "working_day":
                bool(
                    working_day
                )
        }

    # ============================================================
    # DEMO CONTEXT
    # ============================================================

    @classmethod
    def demo_context(cls):
        """
        Return the synthetic energy context required for the
        Campus360 optimization demonstration.

        This does not modify or replace live telemetry.
        """

        return {
            "actual_energy": 185.0,
            "expected_energy": 50.0,
            "occupancy": 22.0,
            "working_day": True,
            "temperature": 33.0,
            "hvac_load": 90.0,
            "hour": 14
        }

    # ============================================================
    # MAIN ANALYSIS
    # ============================================================

    @classmethod
    def analyze(
        cls,
        actual_energy,
        expected_energy=None,
        occupancy=None,
        working_day=None,
        temperature=None,
        hvac_load=None,
        hour=None
    ):
        """
        Perform complete energy context analysis.

        Parameters are configurable so the optimization layer
        can later receive real or simulated context.

        If context values are omitted, the required demo
        scenario is used.
        """

        actual = cls._number(
            actual_energy
        )

        expected = cls._number(
            expected_energy,
            cls.DEFAULT_EXPECTED_ENERGY
        )

        occupancy_value = cls._clamp(
            cls._number(
                occupancy,
                cls.DEFAULT_OCCUPANCY
            ),
            0.0,
            100.0
        )

        working_day_value = (
            cls.DEFAULT_WORKING_DAY
            if working_day is None
            else bool(
                working_day
            )
        )

        temperature_value = cls._number(
            temperature,
            cls.DEFAULT_TEMPERATURE
        )

        hvac_load_value = cls._clamp(
            cls._number(
                hvac_load,
                cls.DEFAULT_HVAC_LOAD
            ),
            0.0,
            100.0
        )

        hour_value = int(
            cls._number(
                hour,
                cls.DEFAULT_HOUR
            )
        )

        hour_value = int(
            cls._clamp(
                hour_value,
                0,
                23
            )
        )

        deviation = cls.calculate_deviation(
            actual,
            expected
        )

        status = cls.determine_context_status(
            deviation_percent=deviation,
            occupancy=occupancy_value,
            temperature=temperature_value,
            hvac_load=hvac_load_value
        )

        flags = cls.build_flags(
            occupancy=occupancy_value,
            working_day=working_day_value,
            temperature=temperature_value,
            hvac_load=hvac_load_value,
            deviation_percent=deviation
        )

        interpretation = cls.build_interpretation(
            actual_energy=actual,
            expected_energy=expected,
            deviation_percent=deviation,
            status=status,
            occupancy=occupancy_value,
            working_day=working_day_value,
            temperature=temperature_value,
            hvac_load=hvac_load_value,
            hour=hour_value
        )

        return {

            "actual_energy":
                round(
                    actual,
                    2
                ),

            "expected_energy":
                round(
                    expected,
                    2
                ),

            "deviation_percent":
                deviation,

            "status":
                status,

            "occupancy":
                round(
                    occupancy_value,
                    2
                ),

            "working_day":
                working_day_value,

            "temperature":
                round(
                    temperature_value,
                    2
                ),

            "hvac_load":
                round(
                    hvac_load_value,
                    2
                ),

            "hour":
                hour_value,

            "flags":
                flags,

            "interpretation":
                interpretation
        }


# ================================================================
# DEMO / QUICK TEST
# ================================================================

if __name__ == "__main__":

    print(
        "=" * 65
    )

    print(
        "        CAMPUS360 ENERGY CONTEXT ANALYSIS"
    )

    print(
        "=" * 65
    )

    # Required demo scenario:
    #
    # Actual energy     = 185 kWh
    # Expected energy   = 50 kWh
    # Occupancy         = 22%
    # Working day       = YES
    # Temperature       = 33 C
    # HVAC load         = 90%
    # Time              = 2 PM

    result = EnergyContextAnalyzer.analyze(
        actual_energy=185,
        expected_energy=50,
        occupancy=22,
        working_day=True,
        temperature=33,
        hvac_load=90,
        hour=14
    )

    print()

    for key, value in result.items():

        print(
            f"{key}: {value}"
        )

    print()

    print(
        "=" * 65
    )

    print(
        "        CONTEXT ANALYSIS COMPLETE"
    )

    print(
        "=" * 65
    )