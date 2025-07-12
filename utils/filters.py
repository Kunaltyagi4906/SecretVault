# utils/filters.py
import re
from markupsafe import Markup

def highlight(text, search):
    if not search:
        return text
    pattern = re.escape(search)
    highlighted = re.sub(f'({pattern})', r'<mark>\1</mark>', text, flags=re.IGNORECASE)
    return Markup(highlighted)
