#!/usr/bin/env python3
from typing import Any, NamedTuple


class Telegram(NamedTuple):
    src: str
    dst: str
    value: Any


def decode_individual_address(individual_address: int) -> str:
    """Decode an individual address into human readable string representation.

    decode_individual_address(4606)
    '1.1.254'

    See also: http://www.openremote.org/display/knowledge/KNX+Individual+Address
    """
    return f"{(individual_address >> 12) & 0x1f}.{(individual_address >> 8) & 0x07}.{(individual_address) & 0xff}"


def decode_group_address(group_address: int) -> str:
    """Decodes a group address into human readable string representation.

    decode_group_address(270)
    '0/1/14'
    """
    return f"{(group_address >> 11) & 0x1f}/{(group_address >> 8) & 0x07}/{(group_address) & 0xff}"


def decode(buf: bytearray) -> Telegram:
    """Decodes a binary telegram in the format:

        2 byte: src
        2 byte: dst
        X byte: data

    Returns a Telegram namedtuple.

    If the data had only 1 bytes the value is either 0 or 1
    In case there was more than 1 byte the value will contain the raw data as
    bytestring.

    decode(bytearray([0x11, 0xFE, 0x00, 0x07, 0x00, 0x83]))
    Telegram(src='1.1.254', dst='0/0/7', value=3)

    decode(bytearray([0x11, 0x08, 0x00, 0x14, 0x00, 0x81]))
    Telegram(src='1.1.8', dst='0/0/20', value=1)

    """
    src = decode_individual_address(buf[0] << 8 | buf[1])
    dst = decode_group_address(buf[2] << 8 | buf[3])

    data = buf[6:]

    value = (data[0] & 0x3F).to_bytes(1, "big") if len(data) == 1 else data[1:]
    return Telegram(src, dst, value)
