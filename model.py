from datetime import datetime
from pydantic import BaseModel

class IncidentsModel(BaseModel): 

    cod_incident: str
    last_update: datetime 
    last_update_description: str | None
    status: str
    operator_name: str | None