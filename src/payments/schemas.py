from pydantic import BaseModel


class PaymentSchema(BaseModel):
    url: str
    id_: int


class PaymentStatus:
    PAID = "paid"
    NOT_PAID = "not_paid"
