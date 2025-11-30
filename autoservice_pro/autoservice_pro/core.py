from datetime import timedelta

class ServiceEstimator:
    """
    Estimate service duration (in minutes) based on service_type and workload.
    """

    BASE_TIMES = {
        "oil_change": 45,
        "tyre_rotation": 60,
        "full_service": 180,
        "inspection": 90,
        "car_wash": 30,
    }

    WORKLOAD_MULTIPLIER = {
        "low": 0.9,
        "medium": 1.0,
        "high": 1.3,
    }

    def estimate_time(self, service_type: str, workload: str = "medium") -> int:
        base = self.BASE_TIMES.get(service_type, 60)
        mult = self.WORKLOAD_MULTIPLIER.get(workload, 1.0)
        return int(base * mult)


def calculate_price(
    service_type: str,
    vehicle_type: str = "sedan",
    add_ons: list | None = None,
) -> float:
    """
    Calculate price based on service_type, vehicle_type and add-ons.
    """

    if add_ons is None:
        add_ons = []

    base_prices = {
        "oil_change": 80.0,
        "tyre_rotation": 60.0,
        "full_service": 250.0,
        "inspection": 100.0,
        "car_wash": 25.0,
    }

    vehicle_multipliers = {
        "sedan": 1.0,
        "hatchback": 0.9,
        "suv": 1.2,
        "truck": 1.4,
        "other": 1.0,
    }

    add_on_prices = {
        "wheel_balancing": 30.0,
        "interior_cleaning": 40.0,
        "polish": 50.0,
    }

    base = base_prices.get(service_type, 60.0)
    vehicle_mult = vehicle_multipliers.get(vehicle_type, 1.0)
    add_total = sum(add_on_prices.get(a, 0.0) for a in add_ons)

    return round(base * vehicle_mult + add_total, 2)
