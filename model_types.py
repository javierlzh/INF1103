"""Explicit saved-record schemas and the numeric-input callback contract."""

from typing import NotRequired, Protocol, TypeGuard, TypedDict, overload


class SupplierData(TypedDict):
    supplier_id: str
    name: str
    contact_email: str


class ProductData(TypedDict):
    id: str
    name: str
    price: float
    stock: int
    supplier: SupplierData
    # The abstract Product supplies common fields; subclasses add these fields.
    type: NotRequired[str]
    weight: NotRequired[float]
    download_size: NotRequired[float]
    billing_cycle: NotRequired[str]


def is_supplier_data(value: object) -> TypeGuard[SupplierData]:
    """Check untrusted JSON before treating it as a supplier record."""
    if not isinstance(value, dict):
        return False
    return all(
        isinstance(value.get(key), str) and bool(value[key].strip())
        for key in ("supplier_id", "name", "contact_email")
    )


def is_product_data(value: object) -> TypeGuard[ProductData]:
    """Validate common fields and the fields used by each product variant."""
    if not isinstance(value, dict):
        return False
    if not all(isinstance(value.get(key), str) for key in ("id", "name", "type")):
        return False
    if type(value.get("price")) not in (int, float) or type(value.get("stock")) is not int:
        return False
    if not is_supplier_data(value.get("supplier")):
        return False
    for key in ("weight", "download_size"):
        if key in value and type(value[key]) not in (int, float):
            return False
    if "billing_cycle" in value and not isinstance(value["billing_cycle"], str):
        return False
    required_fields: dict[str, str] = {
        "physical": "weight", "digital": "download_size", "subscription": "billing_cycle"
    }
    required_field = required_fields.get(value["type"])
    return required_field is None or required_field in value


class ReadNumber(Protocol):
    """Choosing int returns int; choosing float (or omitting it) returns float."""

    @overload
    def __call__(self, prompt: str, number_type: type[int]) -> int: ...

    @overload
    def __call__(self, prompt: str, number_type: type[float] = float) -> float: ...
