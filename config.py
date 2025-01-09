"""config.py"""
import os
import numpy as np


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')

        self.starting = np.datetime64('2022-01-01', '%Y-%m-%d')
        self.at_least = np.datetime64('2025-01-05', '%Y-%m-%d')
