#!/usr/bin/env python3
"""TODO : Desc"""
import re
from typing import List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """init function"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format log message"""
        log_message = super().format(record)
        for field in self.fields:
            log_message = filter_datum(
                [field], self.REDACTION, log_message, self.SEPARATOR)
        return log_message


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
