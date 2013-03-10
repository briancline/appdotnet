def is_sequence(x):
    return (not hasattr(x, 'strip') and
            hasattr(x, '__getitem__') or
            hasattr(x, '__iter__'))
