# Usage

Comparison and testing of the data structures in `jdiff` is performed through one of the built-in `CheckType` type objects, which are explained below in more detail.

A `jdiff` `CheckType` accepts two Python dictionaries as input: the reference object and the comparison object. The reference object is used as the intended or accepted state and its keys and values are compared against the key-value pairs in the comparison object. 

It's worth pointing out that `jdiff` is focused on the comparison of the two objects and the testing of the values, not retrieving the data from the external system.

## Workflow

In summary, the workflow is generally:

1. Get the data from the external system 
2. Define a jmespath expression to Extract the Data for Comparison
3. Extract the key-value pairs with `extract_data_from_json` with the jmespath and data
4. Instantiate the `CheckType`
5. Define the parameters for the check (in the case of more complex `CheckTypes`)
6. Input the parameters and `evaluate`


## Extracting Data For Comparison

Before we get started with the CheckTypes, we've also included a method of extracting portions of the data for comparison. In many cases in data comparison, we aren't interested in the whole piece of data. We've provided this utility to extract subsets of a larger data object. 

## `extract_data_from_json`

As an example, in this case of the object below, we are only interested in comparing the value of a single key-value pair from each item in the interfaces dictionary contained within the response. 

```python
>>> from jdiff import extract_data_from_json
>>> reference_data = {
      "jsonrpc": "2.0",
      "id": "EapiExplorer-1",
      "result": [
        {
          "interfaces": {
            "Management1": {
              "lastStatusChangeTimestamp": 1626247820.0720868,
              "lanes": 0,
              "name": "Management1",
              "interfaceStatus": "connected",
              "autoNegotiate": "success",
              "burnedInAddress": "08:00:27:e6:b2:f8",
              "loopbackMode": "loopbackNone",
              "interfaceStatistics": {
                "inBitsRate": 3582.5323982177174,
                "inPktsRate": 3.972702352461616,
                "outBitsRate": 17327.65267220522,
                "updateInterval": 300,
                "outPktsRate": 2.216220664406746
              }
            }
          }
        }
      ]
    }
```
After getting the response data from an external system, we'll create a query (similar to JMESpath syntax) to extract the key-value pair that we want to use for comparison. With the query and the data, call `extract_data_from_json` to get the subset of data we are interested in using. 

```python
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus]"
>>> reference_value = extract_data_from_json(reference_data, my_jmspath)
>>> reference_value
[{'Management1': {'interfaceStatus': 'connected'}}]
```

This type of logic to extract keys and value from the object is called anchor logic.


# `CheckTypes` Explained

## exact_match

Check type `exact_match` is concerned with the value of the elements within the data structure. The key-value pairs should match between the reference and comparison data. A diff is generated between the two data sets and tested to see whether all the keys and values match.

As some outputs might be too verbose or include fields that constantly change (e.g., interface counter), it is possible to exclude a portion of data traversed by JMESPath by defining a list of excluded keys.

Examples:

```python
>>> from jdiff import CheckType
>>> reference_data = {
      "jsonrpc": "2.0",
      "id": "EapiExplorer-1",
      "result": [
        {
          "interfaces": {
            "Management1": {
              "lastStatusChangeTimestamp": 1626247820.0720868,
              "lanes": 0,
              "name": "Management1",
              "interfaceStatus": "connected",
              "autoNegotiate": "success",
              "burnedInAddress": "08:00:27:e6:b2:f8",
              "loopbackMode": "loopbackNone",
              "interfaceStatistics": {
                "inBitsRate": 3582.5323982177174,
                "inPktsRate": 3.972702352461616,
                "outBitsRate": 17327.65267220522,
                "updateInterval": 300,
                "outPktsRate": 2.216220664406746
              }
            }
          }
        }
      ]
    }
>>> comparison_data = {
      "jsonrpc": "2.0",
      "id": "EapiExplorer-1",
      "result": [
        {
          "interfaces": {
            "Management1": {
              "lastStatusChangeTimestamp": 1626247821.123456,
              "lanes": 0,
              "name": "Management1",
              "interfaceStatus": "down",
              "autoNegotiate": "success",
              "burnedInAddress": "08:00:27:e6:b2:f8",
              "loopbackMode": "loopbackNone",
              "interfaceStatistics": {
                "inBitsRate": 3403.4362520883615,
                "inPktsRate": 3.7424095978179257,
                "outBitsRate": 16249.69114419833,
                "updateInterval": 300,
                "outPktsRate": 2.1111866059750692
              }
            }
          }
        }
      ]
    }

```
Create an instance of `CheckType` object with 'exact_match' as check-type argument.

```python
>>> my_check = CheckType.create(check_type="exact_match")
>>> my_check
>>> <jdiff.check_types.ExactMatchType object at 0x10ac00f10>
```

Use the `evaluate` method to return the result.

```python
>>> result = my_check.evaluate(reference_data, comparison_data)
>>> result
>>> ({'result': {'interfaces': {'Management1': {'lastStatusChangeTimestamp': {'new_value': 1626247821.123456,
      'old_value': 1626247820.0720868},
     'interfaceStatus': {'new_value': 'down', 'old_value': 'connected'},
     'interfaceStatistics': {'inBitsRate': {'new_value': 3403.4362520883615,
       'old_value': 3582.5323982177174},
      'inPktsRate': {'new_value': 3.7424095978179257,
       'old_value': 3.972702352461616},
      'outBitsRate': {'new_value': 16249.69114419833,
       'old_value': 17327.65267220522},
      'outPktsRate': {'new_value': 2.1111866059750692,
       'old_value': 2.216220664406746}}}}}},
 False)
```

As we can see, we return a tuple containing a diff between the pre and post data as well as a boolean for the overall test result. In this case a difference has been found, so the result of the test is `False`.

Let's see a better way to run `exact_match` for this specific case. Because there are a lot of extra key-value pairs, some of which change all the time, we are interested only in `interfaceStatus`. In this case we can use the `extract_data_from_json` utility, to extract only the value from the keys we are interested in and discard the rest.

```python
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus]"
>>> reference_value = extract_data_from_json(reference_data, my_jmspath)
>>> reference_value
[{'Management1': {'interfaceStatus': 'connected'}}]
>>> comparison_value = extract_data_from_json(comparison_data, my_jmspath)
>>> comparison_value
[{'Management1': {'interfaceStatus': 'down'}}]
>>> result = my_check.evaluate(reference_value, comparison_value)
>>> result
({'Management1': {'interfaceStatus': {'new_value': 'down',
    'old_value': 'connected'}}},
 False)
```

In this case, we only want to compare the value of a single key, the `interfaceStatus` key. So we define the JMESPath expression to take the name and the interfaceStatus values from all the interface objects in the data object. 


### Tolerance

The `tolerance` test checks for the deviation between the value or count of the reference and comparison values. A `tolerance` is defined and passed to the check along with the comparison and reference values.

The `tolerance` argument must be a `float > 0`. The calculation is percentage based, and the test of the values may be +/- the `tolerance` percentage.

This check can test whether the difference between two values is within a specified tolerance percentage. It could be useful in cases where values like route metrics or optical power levels fluctuate by a small amount. It might be desirable to treat these values as equal if the deviation is within a given range. You can pass in the result of `len()` to count the number of objects returned within your data.

Let's have a look at a couple of examples:

```python
>>> reference_data = {
...     "global": {
...         "peers": {
...             "10.1.0.0": {
...                 "address_family": {
...                     "ipv4": {
...                         "accepted_prefixes": 900,
...                         "received_prefixes": 999,
...                         "sent_prefixes": 1011
...                     },
...                     "ipv6": {
...                         "accepted_prefixes": 1000,
...                         "received_prefixes": 1000,
...                         "sent_prefixes": 1000
...                     }
...                 },
...                 "description": "",
...                 "is_enabled": True,
...                 "is_up": True,
...                 "local_as": 4268360780,
...                 "remote_as": 67890,
...                 "remote_id": "0.0.0.0",
...                 "uptime": 1783
...             }
...         }
...     }
... }
>>> comparison_data = {
...     "global": {
...         "peers": {
...             "10.1.0.0": {
...                 "address_family": {
...                     "ipv4": {
...                         "accepted_prefixes": 500,
...                         "received_prefixes": 599,
...                         "sent_prefixes": 511
...                     },
...                     "ipv6": {
...                         "accepted_prefixes": 1000,
...                         "received_prefixes": 1000,
...                         "sent_prefixes": 1000
...                     }
...                 },
...                 "description": "",
...                 "is_enabled": True,
...                 "is_up": True,
...                 "local_as": 4268360780,
...                 "remote_as": 67890,
...                 "remote_id": "0.0.0.0",
...                 "uptime": 1783
...             }
...         }
...     }
... }
>>> my_check = CheckType.create("tolerance")
```
We will define a JMESPath expression for the values we want to test and extract from the reference and comparison objects.
```python
>>> my_jmspath = "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]"
>>> reference_value = extract_data_from_json(reference_data, my_jmspath)
>>> reference_value
[{'10.1.0.0': {'accepted_prefixes': 900,
   'received_prefixes': 999,
   'sent_prefixes': 1011}}]
>>> comparison_value = extract_data_from_json(comparison_data, my_jmspath)
[{'10.1.0.0': {'accepted_prefixes': 500,
   'received_prefixes': 599,
   'sent_prefixes': 511}}]
```

Define a tolerance percentage.
```python
my_tolerance=10
```
Pass the extracted values and tolerance as arguments to the `evaluate` method.
```python
>>> actual_results = my_check.evaluate(reference_value, comparison_value, tolerance=my_tolerance)
```
The `tolerance` check returns the values that differ by more than 10%.
```python
>>> actual_results
({'10.1.0.0': {'accepted_prefixes': {'new_value': 500, 'old_value': 900},
   'received_prefixes': {'new_value': 599, 'old_value': 999},
   'sent_prefixes': {'new_value': 511, 'old_value': 1011}}},
 False)
```
The last example fails, because none of the values are within 10% of the `old_value`.

When we switch one of the values (`accepted_prefixes`) to a value within 10%, that value will not be shown, but the test fails because the others are still out of tolerance:

```python
>>> comparison_value[0]['10.1.0.0']['accepted_prefixes'] = 891
>>> comparison_value
[{'10.1.0.0': {'accepted_prefixes': 891,
   'received_prefixes': 599,
   'sent_prefixes': 511}}]
>>> actual_results = my_check.evaluate(reference_value, comparison_value, tolerance=my_tolerance)
>>> actual_results
({'10.1.0.0': {'received_prefixes': {'new_value': 599, 'old_value': 999},
   'sent_prefixes': {'new_value': 511, 'old_value': 1011}}},
 False)
```

Let's increase the tolerance:

```python
>>> my_tolerance=80
>>> actual_results = my_check.evaluate(reference_value, comparison_value, tolerance=my_tolerance)
>>> actual_results
({}, True)
```

### Parameter Match

The `parameter_match` check provides a way to test key-value pairs against baseline values.

The check defines baseline key-value pairs in a Python dictionary. Additionally, mode is set to one of `match` or `no-match`, which specifies whether the data should match the baseline, or not.

The test fails if:

  - Specified key-value pairs in the data do not match the baseline and mode is set to `match`.
  - Specified key-value pairs in the data match the baseline and mode is set to `no-match`.
 
 Any key-value pairs present in the data but not in the baseline are ignored by this check.

In data, this could be a state or status key.

For example, in network data:

```python
>>> actual_data = {
...       "jsonrpc": "2.0",
...       "id": "EapiExplorer-1",
...       "result": [
...         {
...           "interfaces": {
...             "Management1": {
...               "lastStatusChangeTimestamp": 1626247821.123456,
...               "lanes": 0,
...               "name": "Management1",
...               "interfaceStatus": "down",
...               "autoNegotiate": "success",
...               "burnedInAddress": "08:00:27:e6:b2:f8",
...               "loopbackMode": "loopbackNone",
...               "interfaceStatistics": {
...                 "inBitsRate": 3403.4362520883615,
...                 "inPktsRate": 3.7424095978179257,
...                 "outBitsRate": 16249.69114419833,
...                 "updateInterval": 300,
...                 "outPktsRate": 2.1111866059750692
...               }
...             }
...           }
...         }
...       ]
...    }
>>> my_check = CheckType.create("parameter_match")
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus,autoNegotiate]"
>>> actual_value = extract_data_from_json(actual_data, my_jmspath)
```

This test requires a `mode` argument; `match` in this case matches the keys and values in the "params" to the keys and values in the data.
```python
>>> intended_value = {
            "interfaceStatus": "connected", 
            "autoNegotiate": "success"
        }
>>> actual_results = my_check.evaluate(
        intended_value,
        actual_value, 
        mode = "match"
    )
>>> actual_results
({'Management1': {'interfaceStatus': 'down'}}, False)
```

mode: `no-match` - return the keys and values from the test object that do not match the keys and values provided in "params"
```python
>>> actual_results = my_check.evaluate(
        intended_value,
        actual_value, 
        mode = "no-match", 
    )
>>> actual_results
({'Management1': {'autoNegotiate': 'success'}}, False
```

### Regex

The `regex` check type evaluates data against a regular expression passed as an argument to the `evaluate` method. Similarly to `parameter_match` check, the `match` and `no-match` modes are supported.

Let's run an example where we want to check the `burnedInAddress` key has a string representing a MAC address as value.

```python
>>> actual_data = {
...       "jsonrpc": "2.0",
...       "id": "EapiExplorer-1",
...       "result": [
...         {
...           "interfaces": {
...             "Management1": {
...               "lastStatusChangeTimestamp": 1626247821.123456,
...               "lanes": 0,
...               "name": "Management1",
...               "interfaceStatus": "down",
...               "autoNegotiate": "success",
...               "burnedInAddress": "08:00:27:e6:b2:f8",
...               "loopbackMode": "loopbackNone",
...               "interfaceStatistics": {
...                 "inBitsRate": 3403.4362520883615,
...                 "inPktsRate": 3.7424095978179257,
...                 "outBitsRate": 16249.69114419833,
...                 "updateInterval": 300,
...                 "outPktsRate": 2.1111866059750692
...               }
...             }
...           }
...         }
...       ]
...     }
```
We define the regex for matching a MAC address string. Then we define the path query to extract the data and create the check.
```python
>>> mac_regex = "^([0-9a-fA-F]{2}:){5}([0-9a-fA-F]{2})$"
>>> path = "result[*].interfaces.*.[$name$,burnedInAddress]"
>>> check = CheckType.create(check_type="regex")
>>> actual_value = extract_data_from_json(actual_data, path)
>>> actual_value
[{'Management1': {'burnedInAddress': '08:00:27:e6:b2:f8'}}]
>>> result = check.evaluate(mac_regex, actual_value, mode="match")
>>> result
({}, True)
```
And for the `no-match` mode:
```python
>>> result = check.evaluate(mac_regex, actual_value, mode="no-match")
>>> result
({'Management1': {'burnedInAddress': '08:00:27:e6:b2:f8'}}, False)
```


### Operator

The `operator` check is a collection of more specific checks divided into categories. Only one of the specific checks can be selected and used for evaluation when defining `operator`. Here is a summary of the available `operator` categories and individual checks:


#### `in` Operators


1. `is-in`: Check if the specified element string value is included in a given list of strings.
      - `is-in: ["down", "up"]`: check if value is in list (down, up)  


2. `not-in`: Check if the specified element string value is NOT included in a given list of strings.
      - `not-in: ["down", "up"]`: check if value is not in list (down, up) 


3. `in-range`: Check if the value of a specified element is in the given numeric range.
      - `in-range: [20, 70]`: check if value is in range between 20 and 70 


4. `not-in-range`: Check if the value of a specified element is outside of a given numeric range.
      - `not-in-range: [5, 40]`: checks if value is not in range between 5 and 40

#### `bool` Operators

1. `all-same`: Check if all content values for the specified element are the same. It can also be used to compare all content values against another specified element.
    - `all-same: flap-count`: checks if all values of node <flap-count> in given path is same or not.

#### `str` Operators

1. `contains`: determines if an element string value contains the provided test-string value.
    - `contains: "underlay"`: checks if "underlay" is present in given data or not. 

2. `not-contains`: determines if an element string value does not contain the provided test-string value.
    - `not-contains: "overlay"`: checks if "overlay" is present in given node or not.

#### `int`, `float` Operators

1. `is-gt`: Check if the value of a specified element is greater than a given numeric value.
    - `is-gt: 2`: checks if value should be greater than 2  

2. `is-lt`: Check if the value of a specified element is lesser than a given numeric value.
    - `is-lt: 55`: checks if value is lower than 55 or not.  


Examples:

```python
>>> data = {
...     "jsonrpc": "2.0",
...     "id": "EapiExplorer-1",
...     "result": [
...       {
...         "vrfs": {
...           "default": {
...             "peerList": [
...               {
...                 "linkType": "external",
...                 "localAsn": "65130.1100",
...                 "peerAddress": "7.7.7.7",
...                 "lastEvent": "NoEvent",
...                 "bgpSoftReconfigInbound": "Default",
...                 "state": "Connected",
...                 "asn": "1.2354",
...                 "routerId": "0.0.0.0",
...                 "prefixesReceived": 101,
...                 "maintenance": False,
...                 "autoLocalAddress": "disabled",
...                 "lastState": "NoState",
...                 "establishFailHint": "Peer is not activated in any address-family mode",
...                 "maxTtlHops": None,
...                 "vrf": "default",
...                 "peerGroup": "EVPN-OVERLAY-SPINE",
...                 "idleReason": "Peer is not activated in any address-family mode",
...               },
...               {
...                 "linkType": "external",
...                 "localAsn": "65130.1100",
...                 "peerAddress": "10.1.0.0",
...                 "lastEvent": "Stop",
...                 "bgpSoftReconfigInbound": "Default",
...                 "state": "Idle",
...                 "asn": "1.2354",
...                 "routerId": "0.0.0.0",
...                 "prefixesReceived": 50,
...                 "maintenance": False,
...                 "autoLocalAddress": "disabled",
...                 "lastState": "Active",
...                 "establishFailHint": "Could not find interface for peer",
...                 "vrf": "default",
...                 "peerGroup": "IPv4-UNDERLAY-SPINE",
...                 "idleReason": "Could not find interface for peer",
...                 "localRouterId": "1.1.0.1",
...               }
...             ]
...           }
...         }
...       }
...     ]
...   }
```

`operator` checks require a `mode` argument - which specifies the operator logic to apply and `operator_data` required for the mode defined.

```python
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup,vrf,state]"
>>> check_args = {"params": {"mode": "all-same", "operator_data": True}}
>>> check = CheckType.create("operator")
>>> value = extract_data_from_json(data, path)
>>> value
[{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Connected'}}, {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}]
>>> result = check.evaluate(check_args, value)
```
We are looking for peers that have the same peerGroup, vrf, and state. Return peer groups that aren't the same. 
```python
>>> result
([{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE',
    'vrf': 'default',
    'state': 'Connected'}},
  {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE',
    'vrf': 'default',
    'state': 'Idle'}}],
 False)
```

Let's now look to an example for the `in` operator. Keeping the same `data` and class object as above:

```python
>>> check_args = {"params": {"mode": "is-in", "operator_data": [20, 40, 50]}}
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
>>> value = extract_data_from_json(data, path)
>>> value
[{'7.7.7.7': {'prefixesReceived': 101}},
 {'10.1.0.0': {'prefixesReceived': 50}}]
```
We are looking for "prefixesReceived" value in the operator_data list.
```python
>>> result = check.evaluate(check_args, value)
>>> result
([{'7.7.7.7': {'prefixesReceived': 101}}], False)
```

What about `str` operator?

```python
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]"
>>> check_args = {"params": {"mode": "contains", "operator_data": "EVPN"}}
>>> value = extract_data_from_json(data, path)
>>> value
[{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE'}},
 {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE'}}]
>>> result = check.evaluate(check_args, value)
>>> result
([{'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE'}}], False)
```

Can you guess what would be the outcome for an `int`, `float` operator?

```python
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
>>> check_args = {"params": {"mode": "is-gt", "operator_data": 20}}
>>> value = extract_data_from_json(data, path)
>>> value
[{'7.7.7.7': {'prefixesReceived': 101}},
 {'10.1.0.0': {'prefixesReceived': 50}}]
>>> result = check.evaluate(check_args, value)
>>> result
([], True)
```

See `tests` folder in the repo for more examples.
