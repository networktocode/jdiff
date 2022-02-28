class Operator():    
    
    def __init__(self, referance_data, value_to_compare) -> None:
        # [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}, 
        # {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}, 
        # {'10.2.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}, 
        # {'10.64.207.255': {'peerGroup': 'IPv4-UNDERLAY-MLAG-PEER', 'vrf': 'default', 'state': 'Idle'}}]
        self.referance_data_value = list(referance_data.values())[0]
        self.value_to_compare = value_to_compare

    
    def all_same(self):
        list_of_values = list()
        result = list()

        for item in self.value_to_compare:
            for value in item.values():
                # Create a list for compare valiues.
                list_of_values.append(value)

        for element in list_of_values:
            if not element == list_of_values[0]:
                result.append(False)
            else:
                result.append(True)

        if self.referance_data_value and not all(result):
            return (False, self.value_to_compare)
        elif self.referance_data_value and all(result):
            return (True, self.value_to_compare)
        elif not self.referance_data_value and not all(result):
            return (True, self.value_to_compare)
        elif not self.referance_data_value and all(result):
            return (False, self.value_to_compare)


    def contains(self):
        result = list()
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    if self.referance_data_value in evaluated_value:
                        # Create a list for compare valiues.
                        result.append(item)
        if result:
            return (True, result)
        else:
            return (False, result)


    def not_contains(self):
        result = list()
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    if self.referance_data_value not in evaluated_value:
                        # Create a list for compare valiues.
                        result.append(item)
        if result:
            return (True, result)
        else:
            return (False, result)


    def is_gt(self):
        result = list()
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    if evaluated_value > self.referance_data_value:
                        # Create a list for compare valiues.
                        result.append(item)
        if result:
            return (True, result)
        else:
            return (False, result)


    def is_lt(self):
        result = list()
        for item in self.value_to_compare:
            for value in item.values():
                for evaluated_value in value.values():
                    if evaluated_value < self.referance_data_value:
                        # Create a list for compare valiues.
                        result.append(item)
        if result:
            return (True, result)
        else:
            return (False, result)
