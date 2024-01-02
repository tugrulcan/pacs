from sqlmodel import Field

from src.floy.models.base_model import BaseModel


class ReceivedDataBase(BaseModel):
    """
    Base model for received_data abstraction.
    """

    __abstract__ = True

    patient_id: str = Field(
        nullable=False,
        description="The Patient ID of the received_data.",
        index=True,
    )

    patient_name: str = Field(
        nullable=False,
        description="The Patient Name of the received_data.",
    )

    study_instance_uid: str = Field(
        nullable=False,
        description="The Study Instance UID of the received_data.",
        index=True,
    )

    instances_in_series: int = Field(
        nullable=False,
        description="The number of instances in the series.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "patient_id": "1",
                    "patient_name": "John Doe",
                    "study_instance_uid": "234234234",
                    "instances_in_series": 5,
                }
            ]
        }
    }


class ReceivedData(ReceivedDataBase, table=True):
    """
    DB Model for received_data abstraction.
    This model keeps the relationship with the other models.
    """

    __tablename__: str = "received_data"  # type: ignore # noqa

    series_instance_uid: str = Field(
        primary_key=True,
        nullable=False,
        description="The Series Instance UID of the received_data.",
    )


class ReceivedDataCreate(ReceivedDataBase):
    """
    Create model for received_data abstraction.
    """


class ReceivedDataRead(ReceivedDataBase):
    """
    Read model for received_data abstraction.
    """

    series_instance_uid: str


class ReceivedDataUpdate(ReceivedDataBase):
    """
    Update model for received_data abstraction.
    """
