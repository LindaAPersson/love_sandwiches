import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET =GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    get sales figures input from the user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Inside the try, converts all strub values to intregers.
    Raises valueError if string cannot be converted tinto int,
    or if ther arent exactrly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) !=6:
            raise ValueError(
                f"Exactrly 6 values requierd, you provided {len(values)}"
            )
    except ValueError as e:
        print(f'Invalide data: {e}, please try again. \n')
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

"""
Reminder on how to refactor code that are alike

def update_sales_worksheet(data):
    print('updateing')
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print('update sales woksheet')

def update_surplus_worksheet(data):
    print('updating surplus')
    surplus_worksheet = SHEET.worksheet('surplus')
    surplus_worksheet.append_row(data)
    print('surplus updated')
"""

def calculate_surplus_data(sales_row):
    """
    calulate the surplus
    """
    print('calculateing surplus data')
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock [-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Data to get the stock number
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    calculating stock data and addding 10%
    """
    print('Calculating stock data')
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        #if you know how many items you want you can do 
        # average = sum(int_column) = / 5 (5 is an exampel)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data

def get_stock_values(data):
    print('geting stock heading')
    
    headings = SHEET.worksheet("stock").row_values(1)
    
    {headings : data for heding in headings}
    print(headings)




def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, 'stock')
    get_stock_values(data)
    return stock_data
    

print('welcome!')
main()
def get_stock_values(data):
    headings = SHEET.worksheet("stock").row_values(1)
    stock_values = {}
    for i in range(len(headings)):
        stock_values[headings[i]] = stock_data[i]
    
    return stock_values
    
stock_values = get_stock_values(stock_data)
print(stock_values)