from dataclasses import dataclass
from typing import Optional

from sqlalchemy.orm import Session

from src.floy.models.received_data import ReceivedData, ReceivedDataUpdate


@dataclass
class ReceivedDataHandler:
    db_session: Session

    def get_received_data_by_series_instance_uid(
        self, series_instance_uid: str
    ) -> Optional[ReceivedData]:
        """
        Gets a received_data by Series Instance UID
        :param series_instance_uid: Series Instance UID of the received_data
        :return: ReceivedData
        """
        return (
            self.db_session.query(ReceivedData)
            .filter(ReceivedData.series_instance_uid == series_instance_uid)  # type: ignore[arg-type]
            .first()
        )

    def insert(self, received_data: ReceivedData) -> ReceivedData:
        """
        Inserts a received_data into the database
        :param received_data: ReceivedDataBase to insert
        :return: None
        :raises: Exception
        """
        try:
            self.db_session.add(received_data)
            self.db_session.commit()
            self.db_session.refresh(received_data)
            return received_data
        except Exception:
            self.db_session.rollback()
            raise
        finally:
            self.db_session.commit()

    def update(
        self, existing: ReceivedData, updated: ReceivedDataUpdate
    ) -> ReceivedData:
        """
        Updates a received_data in the database
        :param existing: ReceivedData to update
        :param updated: ReceivedDataUpdate to update
        :return: ReceivedData
        :raises: Exception
        """
        try:
            existing.patient_id = updated.patient_id
            existing.patient_name = updated.patient_name
            existing.study_instance_uid = updated.study_instance_uid
            existing.instances_in_series = updated.instances_in_series
            self.db_session.commit()
            self.db_session.refresh(existing)
            return existing
        except Exception:
            self.db_session.rollback()
            raise
        finally:
            self.db_session.commit()
