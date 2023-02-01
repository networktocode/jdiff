"""Choices for LB models."""
from nautobot.utilities.choices import ChoiceSet


class CertAlgorithmChoices(ChoiceSet):
    """Valid choices of certificate signing algorithm."""

    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    MD2 = "md2"
    MD5 = "md5"

    CHOICES = (
        (SHA1, "sha1"),
        (SHA224, "sha224"),
        (SHA256, "sha256"),
        (SHA384, "sha384"),
        (SHA512, "sha512"),
        (MD2, "md2"),
        (MD5, "md5"),
    )


class Protocols(ChoiceSet):
    """Valid choices for protocols."""

    TCP = "tcp"
    UDP = "udp"

    CHOICES = ((TCP, "tcp"), (UDP, "udp"))
