import re # this import is necessary for the regex operations


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