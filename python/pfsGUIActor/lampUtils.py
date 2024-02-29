def getLampLabel(key):
    """
    This function return lamp label for a given mhs key.

    The function maps certain keys to specific lamp labels:
    - 'hgcd' is mapped to 'HgCd'
    - 'hgar' is mapped to 'HgAr'
    - 'halogen' is mapped to 'QTH'

    If the key does not match any of the above, the function returns the key itself, but with the first letter capitalized.

    Parameters:
    key (str): A string representing a lamp key.

    Returns:
    str: The corresponding lamp label.
    """
    if key == 'hgcd':
        label = 'HgCd'
    elif key == 'hgar':
        label = 'HgAr'
    elif key == 'halogen':
        label = 'QTH'
    elif key == 'allFiberLamp':
        label = 'allFiberLamp'
    else:
        label = key.capitalize()

    return label
