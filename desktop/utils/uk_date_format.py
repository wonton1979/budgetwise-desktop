def uk_date_format(standard_date:str):
    if standard_date != "N/A":
        split_date = standard_date.split('-')
        return f'{split_date[2]}/{split_date[1]}/{split_date[0]}'
    else:
        return standard_date
