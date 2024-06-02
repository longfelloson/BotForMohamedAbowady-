import csv
from typing import List

from src import config
from src.subscriptions.models import Subscription

FILE_COLUMNS = ["NUM", "User ID", "STATUS", "SUBSCRIPTION PERIOD"]
KEYS = ['id_', 'user_id', 'status', 'subscription_time']


def update_csv_file(subscriptions: List[Subscription]) -> None:
    """
    Writing info to csv file.
    """
    with open(config.CSV_FILE_PATH, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(FILE_COLUMNS)
        for subscription in subscriptions:
            writer.writerow(subscription.to_dict(KEYS).values())
