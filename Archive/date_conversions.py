from dataclasses import dataclass


@dataclass
class date:
    year: int
    month: int
    day: int


def date_to_string(date: date):
    return f"{date.day}.{date.month}.{date.year}"

def string_to_date(date: str):
    datearr = str.split(".")
    date = date(day=datearr[0],month=datearr[1],year=datearr[2])
    return date

# this converts between string and date types (a custom type)
# allowing for easy storage in database and retrieving from
# a database

