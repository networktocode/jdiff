"""Choices for LB models."""
from nautobot.utilities.choices import ChoiceSet


class Methods(ChoiceSet):
    """Valid choices for LB Methods."""

    ROUNDROBIN = "roundrobin"
    LEASTCONNECTION = "leastconnection"
    LEASTRESPONSETIME = "leastresponsetime"
    URLHASH = "urlhash"
    DOMAINHASH = "domainhash"
    DESTINATIONIPHASH = "destinationiphash"
    SOURCEIPHASH = "sourceiphash"
    SRCIPDESTIPHASH = "srcipdestiphash"
    LEASTBANDWIDTH = "leastbandwidth"
    LEASTPACKETS = "leastpackets"
    SRCIPSRCPORTHASH = "srcipsrcporthash"
    CUSTOMLOAD = "customload"
    LEASTREQUEST = "leastrequest"

    CHOICES = (
        (ROUNDROBIN, "roundrobin"),
        (LEASTCONNECTION, "leastconnection"),
        (LEASTRESPONSETIME, "leastresponsetime"),
        (URLHASH, "urlhash"),
        (DOMAINHASH, "domainhash"),
        (DESTINATIONIPHASH, "destinationiphash"),
        (SOURCEIPHASH, "sourceiphash"),
        (SRCIPDESTIPHASH, "srcipdestiphash"),
        (LEASTBANDWIDTH, "leastbandwidth"),
        (LEASTPACKETS, "leastpackets"),
        (SRCIPSRCPORTHASH, "srcipsrcporthash"),
        (CUSTOMLOAD, "customload"),
        (LEASTREQUEST, "leastrequest"),
    )


class PersistenceType(ChoiceSet):
    """Valid choices for protocols."""

    SOURCEIP = "sourceip"
    COOKIEINSERT = "cookieinsert"
    RULE = "rule"
    NONE = "none"

    CHOICES = ((SOURCEIP, "sourceip"), (COOKIEINSERT, "cookieinsert"), (RULE, "rule"), (NONE, "none"))


class Protocols(ChoiceSet):
    """Valid choices for protocols."""

    TCP = "tcp"
    UDP = "udp"

    CHOICES = ((TCP, "tcp"), (UDP, "udp"))


class MonitorTypes(ChoiceSet):
    """Valid choices for Monitor."""

    PING = "PING"
    TCP = "TCP"
    HTTP = "HTTP"
    TCP_ECV = "TCP-ECV"
    HTTP_ECV = "HTTP-ECV"
    UDP_ECV = "UDP-ECV"
    LDAP = "LDAP"
    SNMP = "SNMP"

    CHOICES = (
        (PING, "PING"),
        (TCP, "TCP"),
        (HTTP, "HTTP"),
        (TCP_ECV, "TCP-ECV"),
        (HTTP_ECV, "HTTP-ECV"),
        (UDP_ECV, "UDP-ECV"),
        (LDAP, "LDAP"),
        (SNMP, "SNMP"),
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
