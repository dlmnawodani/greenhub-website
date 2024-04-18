def to_lower_camel_case(string: str) -> str:
    split_str = string.split("_")
    return split_str[0] + "".join(word.capitalize() for word in split_str[1:])

__all__ = [
    "to_lower_camel_case"
]