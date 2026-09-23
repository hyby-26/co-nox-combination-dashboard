# Data columns keep their raw CSV names (e.g. "NOX"); only what the UI shows is renamed.
_DISPLAY_NAMES = {"NOX": "NOx"}


def display_name(column: str) -> str:
    return _DISPLAY_NAMES.get(column, column)
