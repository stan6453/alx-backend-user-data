#!/usr/bin/env python3
"""TODO : Desc"""
import mysql.connector
import re
from typing import List, Sequence
import logging
from os import getenv

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'name')


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


def get_logger() -> logging.Logger:
    """Creates a new logger using the custom RedactingFormatter as formatter"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    return mysql.connector.connect(
        user=getenv('PERSONAL_DATA_DB_USERNAME'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=getenv('PERSONAL_DATA_DB_HOST'),
        database=getenv('PERSONAL_DATA_DB_NAME')
    )
