#!/usr/bin/env python3
"""TODO : Desc"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message.

    Arguments:
        fields: A list of strings representing the fields to obfuscate.
        redaction: A string representing the value that will be used to
        obfuscate the specified fields.
        message: A string representing the log line that contains the
        data to be obfuscated.
        separator: A string representing the character that separates
        all the fields in the log line.

    Returns:
        str: The log message with the specified fields obfuscated.

    Example:
        >>> fields = ["password", "date_of_birth"]
        >>> message =
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;"
        >>> separator = ';'
        >>> filter_datum(fields, 'xxx', message, separator)
        'name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;'
    """
    return re.sub(fr'\b({"|".join(fields)})=(.*?){separator}',
                  fr'\1={redaction}{separator}', message)

