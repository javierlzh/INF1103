"""Schema for saved product records."""

from typing import NotRequired, TypedDict

from supplier_data import SupplierData


class ProductData(TypedDict):
    """Common saved fields and the fields supplied by product subclasses."""

    id: str
    name: str
    price: float
    stock: int
    supplier: SupplierData
    type: NotRequired[str]
    weight: NotRequired[float]
    download_size: NotRequired[float]
    billing_cycle: NotRequired[str]
