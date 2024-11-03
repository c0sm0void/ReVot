def dict_to_str(items: dict, depth: int = 0, ignore: list = None) -> str:
    """
    Generate a formatted string from a dictionary, handling nested dictionaries and lists.

    Args:
        items (dict): The dictionary to format.
        depth (int): Indentation level for nested dictionaries.
        ignore (list): Keys to exclude from the output.

    Returns:
        str: The formatted string representation of the dictionary.
    """
    ignore = ignore or []
    lines = []  # Collect lines here for efficient joining at the end
    indent = '  ' * depth

    for name, value in items.items():
        # Skip ignored keys or empty values
        if name in ignore or value is None:
            continue

        if isinstance(value, list):
            value_str = ', '.join(map(str, value))
        elif isinstance(value, dict):
            # Recursive call for nested dictionary
            value_str = '\n' + dict_to_str(value, depth + 1, ignore)
        else:
            value_str = str(value)

        # Append the formatted line
        lines.append(f"{indent}{name}: {value_str}")

    return '\n'.join(lines) if lines else ''
