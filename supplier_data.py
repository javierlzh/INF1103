"""Schema for saved supplier records."""

from typing import TypedDict


class SupplierData(TypedDict):
    supplier_id: str
    name: str
    contact_email: str
