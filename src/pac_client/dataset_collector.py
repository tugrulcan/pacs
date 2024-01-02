import time

from pydicom import Dataset
from pydicom.uid import UID


class DatasetCollector:
    """A Dataset Collector is used to build up a list of instances (a DICOM datasets) as they are received by the modality.
    It stores the (during collection incomplete) datasets, the Series (Instance) UID, the time the datasets was last updated
    with a new instance and the information whether the dispatch of the datasets was started.
    """

    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset_collector (instance).

        Args:
            first_dataset (Dataset): The first dataset_collector or the regarding datasets received from the modality.
        """
        self.series_instance_uid: UID = first_dataset.SeriesInstanceUID
        self.datasets: list[Dataset] = [first_dataset]
        self.last_update_time: float = time.time()
        self.dispatch_started: bool = False

    async def add_dataset(self, dataset: Dataset) -> bool:
        """Add a dataset_collector to the datasets collected by this collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset_collector to add.

        Returns:
            bool: `True`, if the Series UID of the dataset_collector to add matched and the dataset_collector was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.datasets.append(dataset)
            self.last_update_time = time.time()
            return True

        return False
