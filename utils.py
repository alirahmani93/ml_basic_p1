import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()
DATASET_FOLDER = os.getenv('DATASET_FOLDER', os.getcwd())
DATASET_FILE = os.getenv('DATASET_FILE')
REPORTS_FOLDER = os.getenv('REPORTS_FOLDER', 'reports')


def import_dataset(folder_name: str = DATASET_FOLDER, filename: str = DATASET_FILE, file_type: str = None, **kwargs):
    read_type = getattr(pd, f'read_{file_type}', )
    return read_type(f"{folder_name}/{filename}.{file_type}", **kwargs)


def import_reports(folder_name: str = REPORTS_FOLDER, filename: str = DATASET_FILE, file_type: str = None, **kwargs):
    if not file_type:
        file_type = filename.split('.')[-1]
        if not file_type:
            raise ValueError("file_type not acceptable")
    read_type = getattr(pd, f'read_{file_type}', )
    return read_type(f"{folder_name}/{filename}.{file_type}", **kwargs)


def save_report(df: pd.DataFrame, file_type: str, filename: str, reports_folder: str = REPORTS_FOLDER, **kwargs):
    save_method = getattr(df, f'to_{file_type}')
    return save_method(f'{reports_folder}/{filename}.{file_type}', **kwargs)
