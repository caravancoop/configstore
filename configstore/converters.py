_true_values = frozenset({"true", "on", "yes", "1"})
_false_values = frozenset({"false", "off", "no", "0", ""})


def asbool(s) -> bool:
    """Interpret string as a true or false value.

    These strings mean true:
        true
        on
        yes
        1

    These strings mean false:
        false
        off
        no
        0

    Case is ignored, you can write "True" or "NO".
    Whitespace is stripped; empty strings mean false.

    A boolean value is returned as-is, to support real booleans
    passed as default value to Store.get_setting.

    Other values will cause a ValueError, to find config
    problems instead of doing something unexpected silently.
    """

    if isinstance(s, bool):
        return s

    s = str(s).strip().lower()
    if s in _true_values:
        return True
    if s in _false_values:
        return False

    raise ValueError(f"impossible to interpret value {s!r} as boolean")
