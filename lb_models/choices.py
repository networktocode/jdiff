"""Choices for LB models."""
from nautobot.utilities.choices import ChoiceSet

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


class ServiceGroupTypes(ChoiceSet):
    """Valid choices for ServiceGroup."""

    TCP = "TCP"
    UDP = "UDP"
    HTTP = "HTTP"
    SSL = "SSL"
    SSL_BRIDGE = "SSL-BRIDGE"
    SSL_TCP = "SSL-TCP"
    ANY = "ANY"

    CHOICES = (
        (TCP, "TCP"),
        (UDP, "UDP"),
        (HTTP, "HTTP"),
        (SSL, "SSL"),
        (SSL_BRIDGE, "SSL-BRIDGE"),
        (SSL_TCP, "SSL_TCP"),
        (ANY, "ANY"),
    )


class ApplicationClassTypes(ChoiceSet):
    """Valid choices for ApplicationClassTypes."""

    PRODUCTION = "Production"
    DEVELOPMENT = "Development"
    TEST = "Test"
    UAT = "UAT"
    NETLAB = "NetLab"

    CHOICES = (
        (PRODUCTION, "Production"),
        (DEVELOPMENT, "Development"),
        (TEST, "Test"),
        (UAT, "UAT"),
        (NETLAB, "NetLab"),
    )


class ApplicationAccessibility(ChoiceSet):
    """Valid choices for ApplicationAccessibility."""

    TR = "TR"
    NTR = "NTR"

    CHOICES = (
        (TR, "TR"),
        (NTR, "NTR"),
    )
