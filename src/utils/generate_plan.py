from typing import Dict
import os
import time

from utils.city_api import get_city_coordinates
from utils.split_dates import split_dates

def generate_plan(plan: Dict):
    my_plan = {}
    for day in plan:
        location = plan[day]["location"]

        coordinates = get_city_coordinates(location, os.getenv("CITY_API_TOKEN"))

        if("-" in day):
            dates = split_dates(day)
            for date in dates:
                my_plan[date] = coordinates
        else:
            my_plan[day] = coordinates

    return my_plan 