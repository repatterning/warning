"""config.py"""
import os


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
        self.storage = os.path.join(self.warehouse, 'sandbox')
        self.s3_parameters_key = 's3_parameters.yaml'
        self.architectures = ['bert', 'distil', 'roberta', 'electra']

        self.prefix = 'sandbox/'


