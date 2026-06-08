def _normalize_text(value):
    cleaned = value.strip().lower()
    cleaned = cleaned.replace("_", "-")
    cleaned = "-".join(cleaned.split())
    return cleaned


def normalize_title(title):
    return _normalize_text(title)


def normalize_tag(tag):
    return _normalize_text(tag)


def preview_pair(title, tag):
    return normalize_title(title) + ":" + normalize_tag(tag)
