from asyncio import Queue
from typing import Optional

from pydicom.dataset import FileMetaDataset
from pydicom.uid import MRImageStorage
from pynetdicom import AE, debug_logger, events, evt
from pynetdicom.ae import ApplicationEntity
from pynetdicom.transport import ThreadedAssociationServer

debug_logger()


class ModalityStoreSCP:
    def __init__(self) -> None:
        self.application_entity: ApplicationEntity = AE(ae_title="STORESCP")
        self.scp_server: Optional[ThreadedAssociationServer] = None
        self.dataset_queue: Queue = Queue()
        self._configure_application_entity()

    def _configure_application_entity(self) -> None:
        """Configure the Application Entity with the presentation context(s)
        which should be supported and start the SCP server."""
        event_handlers = [
            (
                evt.EVT_C_STORE,  # Intervention event type
                self.handle_c_store_event,  # Callable handler function
            )
        ]

        self.application_entity.add_supported_context(MRImageStorage)
        self.scp_server = self.application_entity.start_server(
            address=("127.0.0.1", 6667),
            block=False,
            evt_handlers=event_handlers,
        )
        print("SCP Server started")

    def handle_c_store_event(self, event: events.Event) -> int:
        """Callable handler function used to handle a C-STORE event.

        Args:
            event (Event): Representation of a C-STORE event.

        Returns:
            int: Status Code
        """
        dataset = event.dataset
        dataset.file_meta = FileMetaDataset(event.file_meta)
        print("Received dataset_collector")
        self.dataset_queue.put_nowait(dataset)

        return 0x0000
