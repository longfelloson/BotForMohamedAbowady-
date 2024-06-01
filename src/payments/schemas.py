from pydantic import BaseModel


class PaymentSchema(BaseModel):
    url: str
    id_: int
