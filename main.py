import csv

from inventory import Inventory
from supplier import Supplier
from persistence import INVENTORY_FILE
from file_handling import FileHandling
from product import Product
from product_factory import ProductFactory
from get_positive_float import get_positive_float
from ui import print_menu, read_number, ui_create_order


class Main:
    """Own application state and run the inventory menu."""

    def __init__(self) -> None:
        self.__files: FileHandling = FileHandling()
        self.__inventory: Inventory = Inventory()
        self.__supplier: Supplier | None = None

    def load_products(self, path: str) -> None:
        """Report and skip invalid rows, and always report when loading finishes."""
        if self.__supplier is None:
            if not self.__choose_supplier():
                return
        try:
            file = open(path, newline='', encoding='utf-8-sig')
        except FileNotFoundError:
            print(f'Products file not found: {path}')
        else:
            loaded = 0
            with file:
                reader = csv.reader(file)
                next(reader, None)
                for row_number, row in enumerate(reader, start=2):
                    try:
                        if len(row) != 5:
                            raise ValueError('Each row must contain five columns.')
                        product_type, product_id, name, price, stock_quantity = (value.strip() for value in row)
                        product = ProductFactory.create(product_type, product_id, name, float(price), int(stock_quantity), 0.0, self.__supplier)
                        self.__inventory.add_product(product)
                    except ValueError as error:
                        print(f'Skipping row {row_number}: {error}')
                    else:
                        loaded += 1
            print(f'{loaded} products loaded.')
        finally:
            print('Load attempt finished.')

    def _prompt_load_products(self) -> None:
        path = input("CSV file path [products.csv] (or 'q' to go back): ").strip()
        if path.lower() == "q":
            return
        path = path or "products.csv"
        if not self.__choose_supplier():
            return
        try:
            self.load_products(path)
        except (OSError, UnicodeError, csv.Error) as error:
            print(f"Could not read products file: {error}")

    def __choose_supplier(self) -> bool:
        supplier_id = input("Supplier ID (or 'q' to go back): ").strip()
        if supplier_id.lower() == "q":
            return False
        supplier: Supplier | None = None
        for product in self.__inventory.get_all_products():
            existing_supplier = product.get_supplier()
            if existing_supplier.get_supplier_id() == supplier_id:
                supplier = existing_supplier
                break
        if supplier is None:
            supplier_name = input("Supplier name: ").strip()
            supplier_email = input("Supplier contact email: ").strip()
            try:
                supplier = Supplier(supplier_id, supplier_name, supplier_email)
            except ValueError as error:
                print(f"Cannot load products: {error}")
                return False
        self.__supplier = supplier
        return True

    def __read_non_negative_int(self, prompt: str) -> int:
        return read_number(prompt, int)

    def __read_non_negative_float(self, prompt: str) -> float:
        return read_number(prompt, float)

    def __show_product(self, product: Product) -> None:
        print(product.display_information())
        print(product.get_fulfilment_info())

    def __display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        products = self.__inventory.get_all_products()
        if not products:
            print("No products in inventory.")
        for product in products:
            self.__show_product(product)
        print("-" * 48)

    def __save(self) -> None:
        if self.__files.save_inventory(self.__inventory):
            print(f"\nInventory saved successfully to {INVENTORY_FILE}.")
        else:
            print("\nFailed to save inventory.")

    def __add_product(self) -> None:
        """Interactive UI flow to add any registered product to the inventory polymorphically."""
        print('\nAdd New Product')
        valid_types = list(Product._registry.keys())
        type_prompt = f"Product Type ({'/'.join(valid_types)}) (or 'q' to go back): "
        while True:
            product_type = input(type_prompt).strip().lower()
            if product_type == 'q':
                return
            elif product_type in valid_types:
                break
            print(f"\nInvalid product type. Please enter one of: {', '.join(valid_types)}.\n")
        while True:
            product_id = input("Product ID (or 'q' to go back): ").strip()
            if product_id.lower() == 'q':
                return
            elif self.__inventory.find_product(product_id) is not None:
                print('\nProduct ID already exists.\n')
            elif product_id != '':
                break
        while True:
            name = input("Product name (or 'q' to go back): ").strip()
            if name.lower() == 'q':
                return
            elif name != '':
                break
        price = get_positive_float('Price: ')
        stock = self.__read_non_negative_int('Stock Quantity: ')
        supplier_id = input('Supplier ID: ').strip()
        supplier: Supplier | None = None
        for existing_product in self.__inventory.get_all_products():
            existing_supplier = existing_product.get_supplier()
            if existing_supplier.get_supplier_id() == supplier_id:
                supplier = existing_supplier
                break
        if supplier is None:
            supplier_name = input('Supplier name: ').strip()
            supplier_email = input('Supplier contact email: ').strip()
            if not all((supplier_id, supplier_name, supplier_email)):
                print('Supplier details cannot be empty.')
                return
            try:
                supplier = Supplier(supplier_id, supplier_name, supplier_email)
            except ValueError as error:
                print(f'\nFailed to add supplier: {error}')
                return
        try:
            extra_value: float = 0.0
            billing_cycle: str | None = None
            if product_type == 'physical':
                extra_value = self.__read_non_negative_float('Weight (kg): ')
            elif product_type == 'digital':
                extra_value = self.__read_non_negative_float('Download Size (MB): ')
            elif product_type == 'subscription':
                billing_cycle = input('Billing Cycle (e.g., Monthly/Yearly): ').strip()
            if product_type == "subscription":
                if billing_cycle is None:
                    raise ValueError("Subscription products require a billing cycle.")
                product = ProductFactory.create_subscription(
                    product_id, name, price, stock, billing_cycle, supplier,
                )
            else:
                product = ProductFactory.create(
                    product_type, product_id, name, price, stock, extra_value, supplier,
                )
            self.__inventory.add_product(product)
        except ValueError as error:
            print(f'\nFailed to add product: {error}')
        else:
            print('\nProduct added successfully!')

    def __update_stock(self) -> None:
        """Interactive UI flow to update product stock."""
        print('\nUpdate Stock')
        while True:
            product_id = input("Enter Product ID (or 'q' to go back): ").strip()
            if product_id.lower() == 'q':
                return
            product = self.__inventory.find_product(product_id)
            if product is not None:
                break
            print('\nProduct not found.\n')
        print(f'\nProduct Found: {product.get_name()} (Current Stock: {product.get_stock()})')
        product.get_supplier().display_information()
        new_stock = self.__read_non_negative_int('\nNew Stock Quantity: ')
        try:
            self.__inventory.update_stock(product_id, int(new_stock))
        except (KeyError, ValueError) as error:
            print(f'\nStock update failed: {error}')
        else:
            print('\nStock updated successfully!')

    def __search_product(self) -> None:
        """Interactive UI flow to search and display a product."""
        print('\nSearch Product')
        while True:
            product_id = input("Enter Product ID (or 'q' to go back): ").strip()
            if product_id.lower() == 'q':
                return
            product = self.__inventory.find_product(product_id)
            if product is not None:
                break
            print('\nProduct not found.\n')
        print('\n' + '-' * 48)
        self.__show_product(product)
        print('-' * 48)

    def run(self) -> None:
        """Main execution loop for the Inventory Management System."""
        exit_program: bool = False
        print("=" * 44)
        print("INVENTORY MANAGEMENT SYSTEM")
        print("=" * 44)
        
        self.__inventory, status = self.__files.load_inventory()
        while status == "error":
            print(f"\nCould not load {INVENTORY_FILE}.")
            print("Correct the file and retry, or exit to preserve the saved data.")
            recovery = input("Enter 'r' to retry or 'q' to exit: ").strip().lower()
            if recovery == "r":
                self.__inventory, status = self.__files.load_inventory()
            elif recovery == "q":
                print("Exited. The inventory file was preserved.")
                return
            else:
                print("Please enter 'r' or 'q'.")
        if status == "loaded":
            print(f"\n{INVENTORY_FILE} found. Inventory loaded successfully.")
        elif status == "not_found":
            print(f"\n{INVENTORY_FILE} not found. Starting with empty inventory.")
        elif status == "duplicates":
            print(f"\n{INVENTORY_FILE} found. Duplicate product IDs were skipped.")
        
        print_menu()
        while not exit_program:
            option: str = input("\nEnter option: ").strip()
        
            if option == "1":
                self.__display_all()
            elif option == "2":
                self.__add_product()
            elif option == "3":
                self.__update_stock()
            elif option == "4":
                self.__search_product()
            elif option == "5":
                self.__save()
            elif option == "6":
                if self.__files.save_inventory(self.__inventory):
                    print("\nThank you for using Inventory Management System. Terminated.")
                    exit_program = True
                else:
                    print("\nFailed to save inventory. Please try saving again before exiting.")
            elif option == "7":
                ui_create_order(self.__inventory)
            elif option == "8":
                self._prompt_load_products()
            else:
                print("\nInvalid option. Please enter 1-8.")


if __name__ == "__main__":
    Main().run()
