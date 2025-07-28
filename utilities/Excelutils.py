import openpyxl
from openpyxl import load_workbook

def get_row_count(file, sheet_name):
    wb = load_workbook(file)
    sheet = wb[sheet_name]
    return sheet.max_row

def get_column_count(file, sheet_name):
    wb = load_workbook(file)
    sheet = wb[sheet_name]
    return sheet.max_column

def read_cell(file, sheet_name, row, column):
    wb = load_workbook(file)
    sheet = wb[sheet_name]
    return sheet.cell(row=row, column=column).value

def write_cell(file, sheet_name, row, column, value):
    wb = load_workbook(file)
    sheet = wb[sheet_name]
    sheet.cell(row=row, column=column, value=value)
    wb.save(file)
    wb.close()

def get_data_as_list(file, sheet_name, skip_header=True):
    """
    Reads all rows in the sheet to a list of tuples.
    If skip_header=True, skips the first row (column names).
    Useful for data-driven tests.
    """
    wb = load_workbook(file)
    sheet = wb[sheet_name]
    data = []
    start_row = 2 if skip_header else 1  # Excel is 1-indexed
    for i in range(start_row, sheet.max_row + 1):
        row_data = []
        for j in range(1, sheet.max_column + 1):
            val = sheet.cell(row=i, column=j).value
            row_data.append(val)
        data.append(tuple(row_data))
    wb.close()
    return data
