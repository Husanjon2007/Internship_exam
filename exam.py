import json
from typing import List

class WeatherRecord:
    city_name: str
    temperatures: List[int]
    humidity_values: List[int]
    conditions: List[str]

    def __init__(self, city_name: str, temperatures: List[int], humidity_values: List[int], conditions: List[str]):
        self.city_name = city_name
        self.temperatures = temperatures
        self.humidity_values = humidity_values
        self.conditions = conditions

    def average_temperature(self) -> float:
        return sum(self.temperatures) / len(self.temperatures) if self.temperatures else 0.0

    def highest_temperature(self) -> int:
        return max(self.temperatures) if self.temperatures else 0

    def lowest_temperature(self) -> int:
        return min(self.temperatures) if self.temperatures else 0

    def average_humidity(self) -> float:
        return sum(self.humidity_values) / len(self.humidity_values) if self.humidity_values else 0.0

    def count_condition(self) -> list:
        return [self.conditions.count("Sunny"), self.conditions.count("Cloudy"), self.conditions.count("Rainy")]

    def classification(self) -> str:
        avg_temp = self.average_temperature()
        if avg_temp >= 30:
            return "Hot week"
        elif avg_temp >= 20:
            return "Warm week"
        else:
            return "Cool week"

    def to_dict(self) -> dict:
        return {
            "city_name": self.city_name,
            "temperatures": self.temperatures,
            "humidity_values": self.humidity_values,
            "conditions": self.conditions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WeatherRecord":
        return cls(
            city_name=data.get("city_name", ""),
            temperatures=data.get("temperatures", []),
            humidity_values=data.get("humidity_values", []),
            conditions=data.get("conditions", []),
        )


def print_record_summary(record: WeatherRecord) -> None:
    sunny, cloudy, rainy = record.count_condition()
    print(f"\nCity: {record.city_name}")
    print(f"  Average temperature = {record.average_temperature():.2f}")
    print(f"  Highest temperature = {record.highest_temperature()}")
    print(f"  Lowest temperature = {record.lowest_temperature()}")
    print(f"  Average humidity = {record.average_humidity():.2f}")
    print(f"  Sunny days = {sunny}")
    print(f"  Cloudy days = {cloudy}")
    print(f"  Rainy days = {rainy}")
    print(f"  Classification = {record.classification()}")


def show_all_records(records: list[WeatherRecord]) -> None:
    for record in records:
        print_record_summary(record)


def show_hottest_city(records: list[WeatherRecord]) -> None:
    if not records:
        print("No records available.")
        return
    hottest = max(records, key=lambda record: record.average_temperature())
    print("\nHottest city based on average temperature:")
    print_record_summary(hottest)


def show_high_humidity_cities(records: list[WeatherRecord]) -> None:
    threshold_input = input("Enter humidity threshold (default 65): ").strip()
    threshold = 65
    if threshold_input:
        try:
            threshold = int(threshold_input)
        except ValueError:
            print("Invalid number; using default threshold of 65.")
    high_humidity = [record for record in records if record.average_humidity() >= threshold]
    if not high_humidity:
        print(f"No cities with average humidity >= {threshold}.")
        return
    print(f"\nCities with average humidity >= {threshold}:")
    for record in high_humidity:
        print_record_summary(record)


def save_records_to_json(records: list[WeatherRecord], path: str) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump([record.to_dict() for record in records], handle, indent=2)
    print(f"Saved {len(records)} records to {path}.")


def load_records_from_json(path: str) -> list[WeatherRecord]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return [WeatherRecord.from_dict(item) for item in data]


def show_menu() -> None:
    print("\nWeather Record Menu")
    print("1. Show all weather reports")
    print("2. Show hottest city")
    print("3. Show cities with high humidity")
    print("4. Save report to weekly_weather_report_json")
    print("5. Read report from weekly_weather_report_json")
    print("6. Exit")


def select_city(records: list[WeatherRecord]) -> WeatherRecord | None:
    print("\nSelect a city by number:")
    for index, record in enumerate(records, start=1):
        print(f"{index}. {record.city_name}")

    choice = input("Enter number: ").strip()
    if not choice.isdigit():
        print("Invalid selection. Please enter a number.")
        return None

    index = int(choice) - 1
    if 0 <= index < len(records):
        return records[index]

    print("Selection out of range.")
    return None


def run_menu(records: list[WeatherRecord]) -> None:
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_all_records(records)
        elif choice == "2":
            show_hottest_city(records)
        elif choice == "3":
            show_high_humidity_cities(records)
        elif choice == "4":
            path = "weekly_weather_report_json"
            try:
                save_records_to_json(records, path)
            except OSError as error:
                print(f"Failed to save JSON file: {error}")
        elif choice == "5":
            path = "weekly_weather_report_json"
            try:
                loaded = load_records_from_json(path)
                records.clear()
                records.extend(loaded)
                print(f"Loaded {len(records)} records from {path}.")
            except FileNotFoundError:
                print(f"File not found: {path}")
            except (OSError, json.JSONDecodeError) as error:
                print(f"Failed to read JSON file: {error}")
        elif choice == "6":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    records = []
    try:
        records = load_records_from_json("weekly_weather_report_json")
        print("Loaded records from weekly_weather_report_json.")
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        print("No saved data found, using default records.")
        city_names = ["Tashkent", "Samarqand", "Kokand", "Ferghana", "Andijon", "Namangan"]
        list_temperatures = [
            [35, 32, 33, 31, 29, 33, 37],
            [33, 34, 35, 36, 37, 38, 38],
            [21, 22, 23, 24, 25, 26, 27],
            [19, 18, 17, 16, 15, 16, 17],
            [10, 15, 16, 17, 18, 19, 20],
            [30, 23, 25, 27, 28, 33, 34],
        ]
        humidity_values = [
            [55, 57, 52, 54, 56, 58, 59],
            [60, 62, 61, 63, 64, 65, 66],
            [70, 72, 71, 73, 74, 75, 76],
            [65, 64, 63, 62, 61, 60, 59],
            [80, 82, 81, 83, 84, 85, 86],
            [45, 47, 46, 48, 49, 50, 51],
        ]
        conditions = [
            ["Sunny", "Sunny", "Cloudy", "Rainy", "Sunny", "Sunny", "Cloudy"],
            ["Cloudy", "Sunny", "Sunny", "Sunny", "Sunny", "Sunny", "Sunny"],
            ["Rainy", "Cloudy", "Cloudy", "Sunny", "Sunny", "Cloudy", "Rainy"],
            ["Sunny", "Sunny", "Cloudy", "Cloudy", "Rainy", "Rainy", "Sunny"],
            ["Cloudy", "Cloudy", "Sunny", "Sunny", "Sunny", "Sunny", "Sunny"],
            ["Sunny", "Sunny", "Rainy", "Rainy", "Sunny", "Cloudy", "Sunny"],
        ]
        records = [
            WeatherRecord(city_names[i], list_temperatures[i], humidity_values[i], conditions[i])
            for i in range(len(city_names))
        ]

    run_menu(records)
