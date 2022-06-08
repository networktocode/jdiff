"""Operator diff."""
import operator
from typing import Any, List, Tuple


class Operator:
    """Operator class implementation."""

    def __init__(self, reference_data: Any, value_to_compare: Any) -> None:
        """__init__ method for Operator class."""
        # [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.2.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.64.207.255': {'peerGroup': 'IPv4-UNDERLAY-MLAG-PEER', 'vrf': 'default', 'state': 'Idle'}}]
        self.reference_data = reference_data
        self.value_to_compare = value_to_compare

    def _loop_through_wrapper(self, call_ops: str) -> Tuple[bool, List]:
        """Private wrapper method for operator evaluation based on 'operator' lib.
        Based on value passed to the method, the appropriate operator logic is triggered.

        Args:
            call_ops: operator type parameter.

        Returns:
            dict: result evaluation based on operator type.
        """
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            "is_in": operator.contains,
            "not_in": operator.contains,
            "contains": operator.contains,
            "not_contains": operator.contains,
        }

        result = []
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    # reverse operands: https://docs.python.org/3.8/library/operator.html#operator.contains
                    if call_ops == "is_in":
                        if ops[call_ops](self.reference_data, evaluated_value):
                            result.append(item)
                    elif call_ops == "not_contains":
                        if not ops[call_ops](evaluated_value, self.reference_data):
                            result.append(item)
                    elif call_ops == "not_in":
                        if not ops[call_ops](self.reference_data, evaluated_value):
                            result.append(item)
                    elif call_ops == "in_range":
                        if self.reference_data[0] < evaluated_value < self.reference_data[1]:
                            result.append(item)
                    elif call_ops == "not_range":
                        if not self.reference_data[0] < evaluated_value < self.reference_data[1]:
                            result.append(item)
                    # "<", ">", "contains"
                    elif ops[call_ops](evaluated_value, self.reference_data):
                        result.append(item)
        if result:
            return (result, True)
        return (result, False)

    def all_same(self) -> Tuple[bool, Any]:
        """All same operator typr implementation."""
        list_of_values = []
        result = []

        for item in self.value_to_compare:
            for value in item.values():
                # Create a list for compare values.
                list_of_values.append(value)

        for element in list_of_values:
            if element != list_of_values[0]:
                result.append(False)
            else:
                result.append(True)

        if self.reference_data and not all(result):
            return (self.value_to_compare, False)
        if self.reference_data:
            return (self.value_to_compare, True)
        if not all(result):
            return (self.value_to_compare, True)
        return (self.value_to_compare, False)

    def contains(self) -> Tuple[bool, List]:
        """'Contains' operator caller."""
        return self._loop_through_wrapper("contains")

    def not_contains(self) -> Tuple[bool, List]:
        """'Not contains' operator caller."""
        return self._loop_through_wrapper("not_contains")

    def is_gt(self) -> Tuple[bool, List]:
        """'Is greather than' operator caller."""
        return self._loop_through_wrapper(">")

    def is_lt(self) -> Tuple[bool, List]:
        """'Is lower than' operator caller."""
        return self._loop_through_wrapper("<")

    def is_in(self) -> Tuple[bool, List]:
        """'Is in' operator caller."""
        return self._loop_through_wrapper("is_in")

    def not_in(self) -> Tuple[bool, List]:
        """'Is not in 'operator caller."""
        return self._loop_through_wrapper("not_in")

    def in_range(self) -> Tuple[bool, List]:
        """'Is in range' operator caller."""
        return self._loop_through_wrapper("in_range")

    def not_range(self) -> Tuple[bool, List]:
        """'Is not in range' operator caller."""
        return self._loop_through_wrapper("not_range")
