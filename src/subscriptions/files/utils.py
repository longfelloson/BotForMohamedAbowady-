import csv
from typing import List

from src import config
from src.subscriptions.models import Subscription

FILE_COLUMNS = ["id_", "user_id", "status", "subscription_time"]


def update_cvs_file(subscriptions: List[Subscription]) -> None:
    """
    Writing info to csv file.
    """
    with open(config.CVS_FILE_PATH, mode='w', newline='') as file:
        file.write(' | '.join(FILE_COLUMNS) + '\n')

        for subscription in subscriptions:
            row = subscription.to_dict(FILE_COLUMNS)
            file.write(' '.join(str(row[column]) for column in FILE_COLUMNS) + '\n')
