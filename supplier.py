from typing import TypeGuard

from supplier_data import SupplierData


def is_supplier_data(value: object) -> TypeGuard[SupplierData]:
    """Check untrusted JSON before treating it as a supplier record."""
    if not isinstance(value, dict):
        return False
    return all(
        isinstance(value.get(key), str) and bool(value[key].strip())
        for key in ("supplier_id", "name", "contact_email")
    )


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str) or not contact_email.strip():
            raise ValueError("Supplier contact email cannot be empty.")
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Contact Email: {self.__contact_email}")
    def to_dict(self) -> SupplierData:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email,
        }

    @classmethod
    def from_dict(cls, data: SupplierData) -> "Supplier":
        if any(not isinstance(value, str) or not value.strip() for value in (
            data.get("supplier_id"), data.get("name"), data.get("contact_email")
        )):
            raise ValueError("Supplier requires an ID, name, and contact email.")
        return cls(data["supplier_id"], data["name"], data["contact_email"])
