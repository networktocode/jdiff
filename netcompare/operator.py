"""Operator diff."""
import operator


class Operator:
    """Operator class implementation."""

    def __init__(self, referance_data, value_to_compare) -> None:
        # [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.2.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}},
        # {'10.64.207.255': {'peerGroup': 'IPv4-UNDERLAY-MLAG-PEER', 'vrf': 'default', 'state': 'Idle'}}]
        self.referance_data = referance_data
        self.value_to_compare = value_to_compare

    def _loop_through_wrapper(self, call_ops):
        """Wrappoer method for operator evaluation."""
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
                    # reverse operands (??? WHY ???) https://docs.python.org/3.8/library/operator.html#operator.contains
                    if call_ops == "is_in":
                        if ops[call_ops](self.referance_data, evaluated_value):
                            result.append(item)
                    elif call_ops == "not_contains":
                        if not ops[call_ops](evaluated_value, self.referance_data):
                            result.append(item)
                    elif call_ops == "not_in":
                        if not ops[call_ops](self.referance_data, evaluated_value):
                            result.append(item)
                    elif call_ops == "in_range":
                        if self.referance_data[0] < evaluated_value < self.referance_data[1]:
                            result.append(item)
                    elif call_ops == "not_range":
                        if not self.referance_data[0] < evaluated_value < self.referance_data[1]:
                            result.append(item)
                    # "<", ">", "contains"
                    elif ops[call_ops](evaluated_value, self.referance_data):
                            result.append(item)
        if result:
            return (True, result)
        return (False, result)

    def all_same(self):
        """All same operator implementation."""
        list_of_values = []
        result = []

        for item in self.value_to_compare:
            for value in item.values():
                # Create a list for compare valiues.
                list_of_values.append(value)

        for element in list_of_values:
            if element != list_of_values[0]:
                result.append(False)
            else:
                result.append(True)


        if self.referance_data and not all(result):
            return (False, self.value_to_compare)
        if self.referance_data:
            return (True, self.value_to_compare)
        if not all(result):
            return (True, self.value_to_compare)
        return (False, self.value_to_compare)


    def contains(self):
        """Contains operator implementation."""
        return self._loop_through_wrapper("contains")

    def not_contains(self):
        """Not contains operator implementation."""
        return self._loop_through_wrapper("not_contains")

    def is_gt(self):
        """Is greather than operator implementation."""
        return self._loop_through_wrapper(">")

    def is_lt(self):
        """Is lower than operator implementation."""
        return self._loop_through_wrapper("<")

    def is_in(self):
        """Is in operator implementation."""
        return self._loop_through_wrapper("is_in")

    def not_in(self):
        """Is not in operator implementation."""
        return self._loop_through_wrapper("not_in")

    def in_range(self):
        """Is in range operator implementation."""
        return self._loop_through_wrapper("in_range")

    def not_range(self):
        """Is not in range operator implementation."""
        return self._loop_through_wrapper("not_range")
