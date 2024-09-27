print("This is my first project in python")
class StockItem:
    stock_category = 'Car accessories'
    vat_rate = 17.5

    def __init__(self, quantity, price, stock_code):
        self.__stock_code = stock_code
        self.__quantity_in_stock = quantity
        self.__price_before_vat = price

    # Setter and Getter methods for Stock Code
    def set_stock_code(self, code):
        self.__stock_code = code

    def get_stock_code(self):
        return self.__stock_code

    # Setter and Getter methods for Quantity in Stock
    def set_quantity_in_stock(self, quantity):
        self.__quantity_in_stock = quantity

    def get_quantity_in_stock(self):
        return self.__quantity_in_stock

    # Setter and Getter methods for Price Before VAT
    def set_price_before_vat(self, price):
        self.__price_before_vat = price

    def get_price_before_vat(self):
        return self.__price_before_vat

    # Method to increase stock
    def increase_stock(self, amount):
        if amount < 1 or self.__quantity_in_stock + amount > 100:
            print("Error: Increased item must be greater than or equal to one or exceeds stock limit")
        else:
            self.__quantity_in_stock += amount

    # Method to sell stock
    def sell_stock(self, amount):
        if amount < 1:
            print("Error: Sold item must be greater than or equal to one")
            return False
        elif amount <= self.__quantity_in_stock:
            self.__quantity_in_stock -= amount
            return True
        else:
            print("Error: Not enough stock available")
            return False

    # Getter method for VAT rate
    def get_vat(self):
        return self.vat_rate

    # Setter method for Price Without VAT
    def set_price_without_vat(self, price):
        self.__price_before_vat = price / (1 + self.vat_rate / 100)

    # Getter method for Price Without VAT
    def get_price_without_vat(self):
        return self.__price_before_vat

    # Method to get the formatted string representation of the object
    def __str__(self):
        return f"Stock Code: {self.__stock_code}, " \
               f"Stock Name: {self.get_stock_name()}, " \
               f"Description: {self.get_stock_description()}, " \
               f"Quantity in Stock: {self.__quantity_in_stock}, " \
               f"Price Before VAT: {self.__price_before_vat:.2f}, " \
               f"Price After VAT: {self.get_price_with_vat():.2f}"

    # Default implementation for Stock Name
    def get_stock_name(self):
        return "Unknown Stock Name"

    # Default implementation for Stock Description
    def get_stock_description(self):
        return "Unknown Stock Description"

    # Getter method for Price With VAT
    def get_price_with_vat(self):
        return self.__price_before_vat * (1 + self.vat_rate / 100)


class NavSys(StockItem):
    def __init__(self, quantity, price, stock_code, brand):
        super().__init__(quantity, price, stock_code)
        self.__brand = brand

    # Override method for Stock Name
    def get_stock_name(self):
        return "Navigation system"

    # Override method for Stock Description
    def get_stock_description(self):
        return f"{self.__brand} Sat Nav"

    # Override method to get the formatted string representation of the object
    def __str__(self):
        return f"{super().__str__()}, Brand: {self.__brand}"


# Function to run the tests
def run_tests():
    # Create an instance of StockItem
    stock_item = StockItem(10, 99.99, 'W101')
    print("Creating a stock with 10 units")
    print(stock_item)

    # Increase stock by 10 units
    print("\nIncreasing 10 more units")
    stock_item.increase_stock(10)
    print(stock_item)

    # Sell 2 units
    print("\nSold 2 units")
    stock_item.sell_stock(2)
    print(stock_item)

    # Set new price per unit
    print("\nSet new price 100.99 per unit")
    stock_item.set_price_without_vat(100.99)
    print(stock_item)

    # Attempt to increase 0 units (error case)
    print("\nIncreasing 0 more units")
    stock_item.increase_stock(0)

    # Create an instance of NavSys
    nav_sys_item = NavSys(5, 199.99, 'N101', 'GeoVision')
    print("\nCreating a stock with 5 units Navigation system")
    print(nav_sys_item)

    # Increase NavSys stock by 5 units
    print("\nIncreasing 5 more units")
    nav_sys_item.increase_stock(5)
    print(nav_sys_item)

    # Sell 3 units of NavSys
    print("\nSold 3 units")
    nav_sys_item.sell_stock(3)
    print(nav_sys_item)

    # Set new price per unit for NavSys
    print("\nSet new price 150.99 per unit")
    nav_sys_item.set_price_without_vat(150.99)
    print(nav_sys_item)

# Run the tests
run_tests()

