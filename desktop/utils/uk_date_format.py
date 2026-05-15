def uk_date_format(standard_date:str):
    split_date = standard_date.split('-')
    return f'{split_date[2]}/{split_date[1]}/{split_date[0]}'
