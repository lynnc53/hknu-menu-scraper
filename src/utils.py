# utility function 
from urllib.parse import quote # for URL encoding

def build_url(date_str):
    """
    Given a data string 'YYYY.MM.DD', return a complete URL for that week.
    """
    encoded_date = quote("=" + date_str) # URL encode the date string
    base_url = (
        "https://www.hknu.ac.kr/kor/670/subview.do?"
        "enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvciUyRjIlMkZ2aWV3LmRvJTNGbW9uZGF5"
        + encoded_date +
        "JndlZWslM0RuZXh0JTI2"
    ) # base URL for weekly view 
    return base_url