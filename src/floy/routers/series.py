from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from src.floy.db.db import get_db
from src.floy.models.received_data import ReceivedDataCreate, ReceivedDataRead
from src.floy.services.received_data_service import ReceivedDataService

INTERFACE = "series"

router = APIRouter(
    prefix=f"/{INTERFACE}",
    tags=[INTERFACE.capitalize()],
)


@router.post(
    path="/{series_instance_uid}",
    status_code=status.HTTP_201_CREATED,
    response_model=ReceivedDataRead,
)
def handle_series(
    series_instance_uid: str,
    payload: ReceivedDataCreate,
    db_session: Session = Depends(get_db),
) -> ReceivedDataRead:
    received_data = ReceivedDataService(
        db_session=db_session
    ).process_received_data(
        series_instance_uid=series_instance_uid, payload=payload
    )
    return ReceivedDataRead.from_orm(**received_data.dict())  # type: ignore[pydantic-orm]
