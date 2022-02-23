from unittest import result


class Operator():    
    
    def __init__(self, referance_data, value_to_compare) -> None:
        
        self.referance_data_type = list(referance_data.keys())[0]
        self.referance_data_value = list(referance_data.values())[0]
        self.value_to_compare = value_to_compare

    
    def all_same(self):

        # [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}, 
        # {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}]
        
        index_key = dict()
        list_of_values = list()
        result = list()

        for number, item in enumerate(self.value_to_compare):
            for key, value in item.keys():
                # Create a mapping between index and key: i.e. {'1': '7.7.7.7', '2': '10.1.0.0'}. We will later use to build the result.
                index_key[number] = key
                # Create a list for compare valiues.
                list_of_values.append(value)

        for number,element in enumerate(list_of_values):
            if not element == list_of_values[0]:
                result.append({index_key[number]: element})
        
        if self.referance_data_value and result:
            return (False, result)
        elif self.referance_data_value and not result:
            return (True, result)
        elif not self.referance_data_value and result:
            return (True, result)
        elif not self.referance_data_value and not result:
            return (False, result)

            

        else:
            pass
