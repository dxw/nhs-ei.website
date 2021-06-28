RECENT = "2021-06-14T"

def filter(page):
    try:
        print('get', page.get('date'))
    except:
        pass
    
    try:
        print ('attr', page.date)
    except:
        pass
    
    return False

