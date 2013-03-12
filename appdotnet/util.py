def is_sequence(x):
    """ Returns whether x is a sequence (tuple, list).

    :param x: a value to check
    :returns: (boolean)

    """
    return (not hasattr(x, 'strip') and
            hasattr(x, '__getitem__') or
            hasattr(x, '__iter__'))
