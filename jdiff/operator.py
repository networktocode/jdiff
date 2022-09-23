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

    def _loop_through_wrapper(self, call_ops: str) -> Tuple[List, bool]:
        """Private wrapper method for operator evaluation based on 'operator' lib.

        Based on value passed to the method, the appropriate operator logic is triggered.

        Args:
            call_ops: operator type parameter.

        Returns:
            dict: result evaluation based on operator type.
        """

        def call_evaluation_logic():
            """Operator valuation logic wrapper."""
            # reverse operands: https://docs.python.org/3.8/library/operator.html#operator.contains
            if call_ops == "is_in":
                if not ops[call_ops](self.reference_data, evaluated_value):
                    result.append(item)
            elif call_ops == "not_contains":
                if ops[call_ops](evaluated_value, self.reference_data):
                    result.append(item)
            elif call_ops == "not_in":
                if ops[call_ops](self.reference_data, evaluated_value):
                    result.append(item)
            elif call_ops == "in_range":
                if not self.reference_data[0] < evaluated_value < self.reference_data[1]:
                    result.append(item)
            elif call_ops == "not_in_range":
                if self.reference_data[0] < evaluated_value < self.reference_data[1]:
                    result.append(item)
            # "<", ">", "contains"
            elif not ops[call_ops](evaluated_value, self.reference_data):
                result.append(item)

        ops = {
            ">": operator.gt,
            "<": operator.lt,
            "is_in": operator.contains,
            "not_in": operator.contains,
            "contains": operator.contains,
            "not_contains": operator.contains,
        }

        result = []  # type: List
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    call_evaluation_logic()
        if result:
            return (result, False)
        return (result, True)

    def all_same(self) -> Tuple[Any, bool]:
        """All same operator type implementation."""
        list_of_values = []
        result = []
        for item in self.value_to_compare:
            # Create a list for compare values.
            list_of_values.extend(iter(item.values()))
        for element in list_of_values:
            if element != list_of_values[0]:
                result.append(False)
            else:
                result.append(True)
        if self.reference_data and not all(result):
            return (self.value_to_compare, False)
        if self.reference_data:
            return ([], True)
        if not all(result):
            return ([], True)
        return (self.value_to_compare, False)

    def contains(self) -> Tuple[List, bool]:
        """Contains operator caller."""
        return self._loop_through_wrapper("contains")

    def not_contains(self) -> Tuple[List, bool]:
        """Not contains operator caller."""
        return self._loop_through_wrapper("not_contains")

    def is_gt(self) -> Tuple[List, bool]:
        """Is greather than operator caller."""
        return self._loop_through_wrapper(">")

    def is_lt(self) -> Tuple[List, bool]:
        """Is lower than operator caller."""
        return self._loop_through_wrapper("<")

    def is_in(self) -> Tuple[List, bool]:
        """Is in operator caller."""
        return self._loop_through_wrapper("is_in")

    def not_in(self) -> Tuple[List, bool]:
        """Is not in operator caller."""
        return self._loop_through_wrapper("not_in")

    def in_range(self) -> Tuple[List, bool]:
        """Is in range operator caller."""
        return self._loop_through_wrapper("in_range")

    def not_in_range(self) -> Tuple[List, bool]:
        """Is not in range operator caller."""
        return self._loop_through_wrapper("not_in_range")
