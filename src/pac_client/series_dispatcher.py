import asyncio
import time
from typing import Optional

import httpx
from pydicom import Dataset

from src.floy.models.received_data import ReceivedDataCreate
from src.pac_client.dataset_collector import DatasetCollector
from src.pac_client.scp import ModalityStoreSCP
from src.settings import config


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming datasets (hint: there is no attribute indicating how
    many instances are in a datasets, so you have to wait for some time to find out if a new instance is transmitted).
    For simplification, you can assume that only one dataset is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher."""

        self.loop: asyncio.AbstractEventLoop
        self.modality_scp: ModalityStoreSCP = ModalityStoreSCP()
        self.dataset_collector_dict: dict = {}
        self.client = httpx.AsyncClient()

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether datasets are received from the modality and prints a message
        regularly when no datasets are received.
        """
        while True:
            # Information about Python asyncio: https://docs.python.org/3/library/asyncio.html
            # When datasets are received you should collect and process them
            # (e.g. using `asyncio.create_task(self.run_series_collector()`)
            if self.modality_scp.dataset_queue.empty():
                print("No datasets left to process")
            else:
                print(
                    "Found new dataset_collector/s, processing...",
                    self.modality_scp.dataset_queue.qsize(),
                )
                await asyncio.create_task(self.run_series_collectors())

            await asyncio.sleep(0.2)
            await asyncio.create_task(self.dispatch_dataset_collector())

    async def run_series_collectors(self) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled."""
        print("Running series collectors")
        dataset: Dataset = await self.modality_scp.dataset_queue.get()
        dataset_collector: Optional[
            DatasetCollector
        ] = self.dataset_collector_dict.get(dataset.SeriesInstanceUID, None)
        if dataset_collector is None:
            print("Creating new dataset_collector")
            dataset_collector = DatasetCollector(dataset)
            self.dataset_collector_dict[
                dataset.SeriesInstanceUID
            ] = dataset_collector
        else:
            print("Adding dataset_collector to existing collector")
            await dataset_collector.add_dataset(dataset)

    async def dispatch_dataset_collector(self) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset_collector collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the datasets collector hasn't had an update for a long enough timespan and send the datasets to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server
        maximum_wait_time_in_seconds = 5
        if len(self.dataset_collector_dict) == 0:
            return

        for collector in self.dataset_collector_dict.values():
            if (
                collector is None
                or collector.dispatch_started
                or len(collector.datasets) < 1
            ):
                continue
            if (
                time.time() - collector.last_update_time
                > maximum_wait_time_in_seconds
            ):
                await asyncio.create_task(
                    self.send_dataset_to_server(dataset_collector=collector)
                )

    async def send_dataset_to_server(
        self, dataset_collector: DatasetCollector
    ) -> None:
        print("Sending dataset_collector to server")
        dataset_collector.dispatch_started = True

        payload: ReceivedDataCreate = ReceivedDataCreate(
            patient_id=dataset_collector.datasets[0].PatientID,
            patient_name=dataset_collector.datasets[0].PatientName.family_name
            + " "
            + dataset_collector.datasets[0].PatientName.given_name,
            study_instance_uid=dataset_collector.datasets[0].StudyInstanceUID,
            instances_in_series=len(dataset_collector.datasets),
        )

        try:
            # Make a POST request to the server with the payload using httpx
            response = await self.client.post(
                url=f"http://{config.API_HOST}:{config.API_PORT}/series/{dataset_collector.series_instance_uid}",
                json=payload.dict(),
            )
            print(response.status_code)
            self.dataset_collector_dict[
                dataset_collector.series_instance_uid
            ] = None
            print("Collector dispatched")
        except Exception as e:
            print("Error while dispatching collector")
            print(e)
            return
        finally:
            dataset_collector.dispatch_started = False
