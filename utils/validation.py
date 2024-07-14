from datetime import datetime

def validate_date(date):
    try:
        date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect date format. Please use 'yyyy-mm-dd'.")