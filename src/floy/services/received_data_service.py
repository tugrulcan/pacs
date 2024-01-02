from dataclasses import dataclass
from typing import Optional

from sqlmodel import Session

from src.floy.db.handlers.received_data_handler import ReceivedDataHandler
from src.floy.models.received_data import (
    ReceivedData,
    ReceivedDataCreate,
    ReceivedDataUpdate,
)


@dataclass
class ReceivedDataService:
    db_session: Session

    def process_received_data(
        self,
        series_instance_uid: str,
        payload: ReceivedDataCreate,
    ) -> ReceivedData:
        """
        Handles transfers in bulk
        :param series_instance_uid:
        :param payload: Payload with transfers
        :return: None
        :raises: HTTPException, ValidationError
        """

        received_data_handler: ReceivedDataHandler = ReceivedDataHandler(
            db_session=self.db_session,
        )
        try:
            received_data: Optional[
                ReceivedData
            ] = received_data_handler.get_received_data_by_series_instance_uid(
                series_instance_uid=series_instance_uid
            )
            if received_data is None:
                received_data = received_data_handler.insert(
                    received_data=ReceivedData(
                        series_instance_uid=series_instance_uid,
                        patient_id=payload.patient_id,
                        patient_name=payload.patient_name,
                        study_instance_uid=payload.study_instance_uid,
                        instances_in_series=payload.instances_in_series,
                    )
                )
            else:
                received_data_handler.update(
                    existing=received_data,
                    updated=ReceivedDataUpdate(**payload.dict()),
                )
        except Exception:
            self.db_session.rollback()
            raise

        return received_data
