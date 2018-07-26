def positioned(rect, **position):
    """
    Return a copy of `rect` positioned like `image.get_rect(**position)` does.
    """
    if not position:
        raise ValueError("Expected at least one `rect` attribute to position on.")
    rect = rect.copy()
    for name, value in position.items():
        setattr(rect, name, value)
    return rect
