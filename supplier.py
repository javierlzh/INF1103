class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.__supplier_id = supplier_id
        self.__name = name
        self.__contact_email = contact_email

    def get_supplier_id(self):
        return self.__supplier_id

    def get_name(self):
        return self.__name

    def get_contact_email(self):
        return self.__contact_email

    def display_information(self):
        print(f"Supplier ID: {self.__supplier_id} | Name: {self.__name} | Contact Email: {self.__contact_email}")