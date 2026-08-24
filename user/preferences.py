def get_target_position() -> str:
    """
    Get the user's desired job position.
    """

    position = input(
        "What job position are you interested in? "
    ).strip()

    if not position:
        raise ValueError("Job position cannot be empty.")

    return position