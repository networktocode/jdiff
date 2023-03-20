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


class HealthMonitorTypes(ChoiceSet):
    """Valid choices for HealthMonitor."""

    PING = "PING"
    TCP = "TCP"
    HTTP = "HTTP"
    TCP_ECV = "TCP-ECV"
    HTTP_ECV = "HTTP-ECV"
    UDP_ECV = "UDP-ECV"
    LDAP = "LDAP"

    CHOICES = (
        # (PING, "PING"),
        # (TCP, "TCP"),
        (HTTP, "HTTP"),
        # (TCP_ECV, "TCP-ECV"),
        # (HTTP_ECV, "HTTP-ECV"),
        # (UDP_ECV, "UDP-ECV"),
        # (LDAP, "LDAP"),
    )
