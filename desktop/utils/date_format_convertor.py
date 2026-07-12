from datetime import date

def uk_date_format(standard_date:str):
    if standard_date != "N/A":
        split_date = standard_date.split('-')
        return f'{split_date[2]}/{split_date[1]}/{split_date[0]}'
    else:
        return standard_date

def long_date_format(standard_date:str):

    if standard_date != "N/A":
        split_date = standard_date.split('-')
        long_date = date(int(split_date[0]), int(split_date[1]), int(split_date[2])).strftime("%d %b %Y")
        return long_date
    else:
        return standard_date