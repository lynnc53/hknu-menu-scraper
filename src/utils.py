# helper functions (e.g. extract_main_menu)
from datetime import datetime, timedelta
import re # this import is necessary for the regex operations
import pandas as pd 

def extract_main_menu(menu_items):
    """
    Extract the main menu from the menu items string.
    If the first item is '백미밥', return the next item.
    Otherwise, return the first item.
    """
    # Check if menu_items is empty or contains a placeholder
    if not menu_items or menu_items.strip() in ["등록된 식단내용이(가) 없습니다.", "미운영"]:
        return menu_items.strip()

    # Split items and remove surrounding whitespace
    items = [item.strip() for item in menu_items.split(",") if item.strip()]
    if not items:
        return ""

    # Logic to skip '백미밥' if it's first
    candidate = items[1] if items[0].startswith("백미밥") and len(items) > 1 else items[0]

    # Remove anything in parentheses, e.g., (돈:국산)
    main_menu_cleaned = re.sub(r"\([^)]*\)", "", candidate).strip()

    return main_menu_cleaned


def extract_exam_content(date_tags, content_tags):
    exam_schedule = []
    for date_tag, content_tag in zip(date_tags, content_tags):
        raw_date = date_tag.get_text(strip=True)
        content_text = content_tag.get_text(strip=True)

        # Check if it's a date range: MM.DD ~ MM.DD
        match_range = re.search(r'(\d{2})[.-](\d{2}).*~.*(\d{2})[.-](\d{2})', raw_date)
        if match_range:
            start_month, start_day, end_month, end_day = match_range.groups()
            start_date = datetime.strptime(f"2025-{start_month}-{start_day}", "%Y-%m-%d")
            end_date = datetime.strptime(f"2025-{end_month}-{end_day}", "%Y-%m-%d")

            current_date = start_date
            while current_date <= end_date:
                exam_schedule.append({
                    "Date": current_date.date(),
                    "Content": content_text
                })
                current_date += timedelta(days=1)
        else:
            # Single date case
            match = re.search(r'(\d{2})[.-](\d{2})', raw_date)
            if not match:
                print(f"Skipping unrecognized date format: {raw_date}")
                continue

            month, day = match.groups()
            date_str = f"2025-{month}-{day}"
            try:
                date_obj = pd.to_datetime(date_str)
                if 3 <= date_obj.month <= 6:
                    exam_schedule.append({
                        "Date": date_obj.date(),
                        "Content": content_text
                    })
            except Exception as e:
                print(f"Failed to parse date '{date_str}': {e}")
                continue

    return exam_schedule 

