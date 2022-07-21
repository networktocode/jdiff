# netcompare

`netcompare` is a lightweight Python library allowing you to examine structured data. `netcompare` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key values.

| Przemek: Is "netcompare" what we want the library to be named? It seems to me that Netcompare or NetCompare would look better in a sentence.

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](#customized-jmespath).

| Przemek: Would be helpful to add a section on the use cases for the library. If our target audience is Network Automation Engineers we should have a few bullet points with example scenarios. If it's more generic then we should have scenarios drawn from different domains.

## Getting started

| Przemek: Reading through docs I can see there are a lot of moving parts. We should create getting started section where we go through a simple example from start to finish.

## Usage

A `netcompare` Check accepts two objects as input: the reference object, and the comparison object. The reference object is used as the intended or accepted state and its keys and values are compared against the comparison object.

| Przemek: At this point in the docs I'd like some diagram, or at least an overview of what I need to get started. We should provide a high level outline of how Netcompare works and what its components are.

| Przemek: We use term "object", how does this look like? Do they need to come in a specific encoding or format? Is it a Python object or a JSON object, or something else?

| Przemek: How do I pass the data to Netcompare?

`netcompare` does not collect the data for you, it simply works on data passed into it. This allows for maximum flexibility in collecting the data. 

For instance, the reference state can be collected from the network directly using any method that returns structured data: Ansible, NAPALM, Nornir to name a few. You could also choose to generate the reference state from an SoT, such as [Nautobot](https://github.com/nautobot/nautobot/), and have a true intended state.

`netcompare` is perfectly suited to work with data gathered from network devices via show commands, Ansible playbooks, as well as in applications such as [Nautobot](https://github.com/nautobot/nautobot/), or [Netbox](https://github.com/netbox-community/netbox). `netcompare` is focused on being the 'plumbing' behind a full network automation validation solution. 

| Przemek: Sounds like Netcompare is a generic solution, but we envision it to be mostly used in network automation.

### Testing data structures

| Przemek: Up until this point we talk about "comparing" and it's not clear what it means to "test" a data structure. Is there a distinction?

| Przemek: Add a sentence about what tests are. Are they a feature of Netcompare? I feel that we're providing reference for tests without introducing them properly.

Briefly, these tests, or `CheckTypes`, are provided to test the objects, to aide in determining the status of the data. 

| Przemek: What does it mean to determine status of the data? Where do `CheckTypes` come from? Also we are now talking about "checks". Would it make sense to standardize on one term?

| Przemek: What are the things below? Types of checks, arguments to a function?

- `exact_match`: the keys and values much match, exactly, between the two objects
- `tolerance`: the keys must match and the values can differ according to the 'tolerance' value provided
- `parameter_match`: a reference key and value is provided and its presence (or absence) is checked in the provided object
- `regex`: a reference regex pattern is provided which is used to find a match in the provided object
- `operator`: similar to parameter match, but the reference includes several different possible operators: 'in', 'bool', 'string', and numerical comparison with 'int' and 'float' to check against

`CheckTypes` are explained in more detail in the [CheckTypes Explained section](#check-types-explained).


## Workflow

| ![netcompare workflow](./docs/images/workflow.png) |
|:---:|
| **`netcompare` workflow** |

| Przemek: I think this diagram would work better if it were wide, rather than tall. Netcompare name should match the name we choose for this library (e.g. Netcompare instead of NETCOMPARE). The individual Netcompare components are difficult to read in the vertical orientation.


1. The reference state object is assembled. The structured data may be collected from:

    - an SoT
    - Directly from the network using any Automation that returns structured data

2. The Network Engineer makes changes to the network, whether it is an upgrade, peering change, or migration.
3. The comparison state is collected, typically directly from the network, but any method is acceptable.
4. The reference state is then compared to the current state using the netcompare library.

| Przemek: This doesn't seem like a generic enough workflow. Ideally replace it using neutral, i.e. not-network related, terms.

## Library Architecture

| ![netcompare HLD](./docs/images/hld.png) |
|:---:|
| **`netcompare` architecture** |

An instance of `CheckType` object must be created first before passing one of the below check types as an argument:

| Przemek: I don't think that is correct. You call `init` method on the class directly and pass it the type of the check. This then returns concrete class implementing `CheckType` interface.

- `exact_match`
- `tolerance`
- `parameter_match`
- `regex`
- `operator`

| Przemek: Perhaps create a table showing how each of the arguments maps to a concrete class?


```python
my_check = "exact_match"
check = CheckType.init(my_check)
```

| Przemek: Where does the `CheckType` is imported from? We should show that.
| Przemek: I don't think `init` is a good name for the factory method. This reads as being related to `__init__`. I would suggest using `create` or similar name to make it clear that the `CheckType` class is an object factory.

Next, define a JSON object as reference data, as well as a JMESPath expression to extract the value wanted and pass them to `get_value` method. `netcompare` extends the JMESPath syntax, see [Customized JMESPath](#customized-jmespath) for details.

```python
bgp_pre_change = "./pre/bgp.json"
bgp_jmspath_exp =  "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]"
pre_value = check.get_value(bgp_pre_change, bgp_jmspath_exp)
```

| Przemek: Does the JSON object have to be on the disk? Can it be an in-memory object? Does it have to a JSON object at all? Can it be a dictionary, or a dictionary-like object?

Once the pre-change values are extracted, we would need to evaluate it against our post-change value. In case of check-type `exact_match` our post-value would be another json object:

```python
bgp_post_change = "./post/bgp.json"
post_value = check.get_value(bgp_post_change, bgp_jmspath_exp)
```

Each check type expects different types of arguments. For example: check type `tolerance` needs a `tolerance` argument, Whereas `parameters` expects a dictionary.

Now that we have pre and post data, we use `evaluate` method to compare them which will return our evaluation result.

| Przemek: "pre" and "post" data doesn't flow very well.

```python
results = check.evaluate(post_value, pre_value, **evaluate_args)
```

## Customized JMESPath

Since `netcompare` works with json objects as data inputs, JMESPath was the obvious choice for traversing the data and extracting the value(s) to compare.

However, JMESPath comes with a limitation where is not possible to define a `key` to which the `value` belongs to.

| Przemek: `key` and `value` are confusing here. This implies parent-child relationship but the example shows two keys, and their values, at the same level of hierarchy. I think something along the lines of "define relationship between two keys and their values" would work better.

Below is the output of `show bgp`.

```json
{
  "result": [
    {
      "vrfs": {
        "default": {
          "peerList": [
            {
              "linkType": "external",
              "localAsn": "65130.1100",
              "prefixesSent": 50,
              "receivedUpdates": 0,
              "peerAddress": "7.7.7.7",
              "state": "Idle",
              "updownTime": 1394,
              "asn": "1.2354",
              "routerId": "0.0.0.0"
            },
            {
              "linkType": "external",
              "localAsn": "65130.1100",
              "receivedUpdates": 0,
              "peerAddress": "10.1.0.0",
              "state": "Connected",
              "updownTime": 1394,
              "asn": "1.2354",
              "routerId": "0.0.0.0"
            }
          ]
        }
      }
    }
  ]
}
```
A JMESPath expression to extract `state` is shown below.

```python
"result[0].vrfs.default.peerList[*].state
```

...which will return

```python
["Idle", "Connected"]
```

How can we show that `Idle` is related to peer `7.7.7.7` and `Connected` to peer `10.1.0.0` ?

We could index the output but that would require some post-processing of the data. For that reason, `netcompare` uses a customized version of JMESPath where it is possible to define a reference key for the value(s) wanted. The reference key must be within `$` sign anchors and defined in a list, together with the value(s):

| Przemek: What does it mean "customized"? Is this a fork or a hook into JMESPath?

```python
"result[0].vrfs.default.peerList[*].[$peerAddress$,state]
```

That  would give us...

```python
{"7.7.7.7": ["Idle"], "10.1.0.0": ["Connected"]}

```

## `CheckTypes` Explained

### exact_match

Check type `exact_match` is concerned about the value of the elements within the data structure. The key/values should match between the pre and post values. A diff is generated between the two data sets.
As some outputs might be too verbose or include fields that constantly change (i.e. interface counter), it is possible to exclude a portion of data traversed by JMESPath by defining a list of keys that we want to exclude.

| Przemek: Pre and post terminology is confusing. We should use more intuitive names.

| Przemek: `get_value` is used without prior introduction. At this stage I'm not sure where this comes from, what it does, and what arguments does it accept.

Examples:


```python
>>> from netcompare import CheckType
>>> pre_data = {
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
>>> post_data = {
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
>>> my_jmspath = "result[*]"
>>> exclude_fields = ["interfaceStatistics", "lastStatusChangeTimestamp"]
>>> # Create an instance of CheckType object with 'exact_match' as check-type argument.
>>> my_check = CheckType.init(check_type="exact_match")
>>> my_check
>>> <netcompare.check_types.ExactMatchType object at 0x10ac00f10>
>>> # Extract the wanted value from pre_dat to later compare with post_data. As we want compare all the body (excluding "interfaceStatistics"), we do not need to define any reference key
>>> pre_value = my_check.get_value(output=pre_data, path=my_jmspath, exclude=exclude_fields)
>>> pre_value
>>> [{'interfaces': {'Management1': {'lastStatusChangeTimestamp': 1626247820.0720868, 'lanes': 0, 'name': 'Management1', 'interfaceStatus': 'connected', 'autoNegotiate': 'success', 'burnedInAddress': '08:00:27:e6:b2:f8', 'loopbackMode': 'loopbackNone'}}}]
>>> post_value = my_check.get_value(output=post_data, path=my_jmspath, exclude=exclude_fields)
>>> post_value
>>> [{'interfaces': {'Management1': {'lastStatusChangeTimestamp': 1626247821.123456, 'lanes': 0, 'name': 'Management1', 'interfaceStatus': 'down', 'autoNegotiate': 'success', 'burnedInAddress': '08:00:27:e6:b2:f8', 'loopbackMode': 'loopbackNone'}}}]
>>> # The pre_value is our intended state for interface Management1, therefore we will use it as reference data. post_value will be our value_to_compare as we want compare the actual state of our interface Management1 (perhaps after a network maintenance) with the its status before the change.
>>> result = my_check.evaluate(value_to_compare=post_value, reference_data=pre_value)
>>> result
>>> ({'interfaces': {'Management1': {'interfaceStatus': {'new_value': 'down', 'old_value': 'connected'}}}}, False)
```

| Przemek: Why is the argument to `get_value` named `output` ? We are passing data structure to it, so perhaps `input` or `data`?

| Przemek: I'm also not sure about `value_to_compare` and `reference_data` arguments.

As we can see, we return a tuple containing a diff between the pre and post data as well as a boolean for the overall test result. In this case a difference has been found so the status of the test is `False`.

Let's see a better way to run `exact_match` for this specific case. Since we are interested in `interfaceStatus` only we could write our JMESPath expression as:

```python
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus]"
>>> pre_value = my_check.get_value(output=pre_data, path=my_jmspath)
>>> pre_value
['connected']
>>> post_value = my_check.get_value(output=post_data, path=my_jmspath)
>>> post_value
['down']
>>> result = my_check.evaluate(value_to_compare=post_value, reference_data=pre_value)
>>> result
({"Management1": {"interfaceStatus": {"new_value": "connected", "old_value": "down"}}}, False)
```

| Przemek: The above example doesn't seem to match the latest version of the library, see my test below:

```
>>> my_check = CheckType.init(check_type="exact_match")
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus]"
>>> pre_value = my_check.get_value(output=pre_data, path=my_jmspath)
>>> pre_value
[{'Management1': {'interfaceStatus': 'connected'}}]
>>> post_value = my_check.get_value(output=post_data, path=my_jmspath)
>>> post_value
[{'Management1': {'interfaceStatus': 'down'}}]
>>> result = my_check.evaluate(value_to_compare=post_value, reference_data=pre_value)
>>> result
({'Management1': {'interfaceStatus': {'new_value': 'down', 'old_value': 'connected'}}}, False)
```

Targeting only the `interfaceStatus` key, we would need to define a reference key (in this case `$name$`), we would not define any exclusion list. 

| Przemek: Reword the above. One possibility: "Using a reference key `$name$` we can ask for specific child key, here `interfaceStatus`. In this case exclusion list is no longer needed."

The anchor logic for the reference key applies to all check-types available in `netcompare`

| Przemek: What is "anchor logic"?

### Tolerance

The `tolerance` test defines a percentage of differing `float()` between pre and post checks numeric value. The threshold is defined as a percentage that can be different either from the value stated in pre and post fields. 

| Przemek: This doesn't read very well. What does the `tolerance` check tests for? Looking at source code it seems we're checking if the deviation(variation) between the actual and expected value is within the percentage tolerance.

The threshold must be `float > 0`, is percentge based, and will be counted as a range centered on the value in pre and post.

| Przemek: Use `tolerance percentage` to be consistent, as that follows the name of the argument. What does this mean: "range centered on the value in pre and post" ?

Let's have a look at a couple of examples:

```python
>>> pre_data = {
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
>>> post_data = {
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
>>> my_check = CheckType.init(check_type="tolerance")
>>> my_jmspath = "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes,sent_prefixes]"
>>> # Tolerance define as 10% delta between pre and post values
>>> my_tolerance_arguments = {"tolerance": 10}
>>> pre_value = my_check.get_value(pre_data, my_jmspath)
>>> post_value = my_check.get_value(post_data, my_jmspath)
>>> actual_results = my_check.evaluate(post_value, pre_value, **my_tolerance_arguments)
>>> # Netcompare returns the value that are not within the 10%
>>> actual_results
({'10.1.0.0': {'accepted_prefixes': {'new_value': 500, 'old_value': 900}, 'received_prefixes': {'new_value': 599, 'old_value': 999}, 'sent_prefixes': {'new_value': 511, 'old_value': 1011}}}, False)
>>> # Let's difine a higher tolerance 
>>> my_tolerance_arguments = {"tolerance": 80}
>>> # In this case, all the values are within the 80% so the check is passed.
>>> actual_results = my_check.evaluate(post_value, pre_value, **my_tolerance_arguments)
>>> actual_results
({}, True)
```

| Przemek: `**my_tolerance_arguments` is not very user friendly. I see `tolerance` is just a standard keyword argument. So we should present examples with `actual_results = my_check.evaluate(post_value, pre_value, tolerance=my_tolerance)`, where `my_tolerance=80` for example.

This test can test the tolerance for changing quantities of certain things such as routes, or L2 or L3 neighbors. It could also test actual outputted values such as transmitted light levels for optics.

| Przemek: "This check can test if the difference between two values is within a specified tolerance percentage. It could be useful in cases where values like route metrics or optical power levels fluctuate by a small amount. It might be desirable to treat these values as equal if the deviation is within a given range."

### Parameter match

The `parameter_match` check provides a way to match keys and values in the output with known good values. 

| Przemek: The `parameter_match` check provides a way to test key/value pairs against baseline values.

The check defines baseline key/value pairs in a Python dictionary. Additionally, mode is set to one of `match` or `no-match`, which specifies if the data should match the baseline, or not.

The test fails if:

  - Specified key/value pairs in the data do not match the baseline and mode is set to `match`.
  - Specified key/value pairs in the data match the baseline and mode is set to `no-match`.
 
 Any key/value pairs present in the data but not in the baseline are ignored by this check.

Examples:

```python
>>> post_data = {
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
>>> my_check = CheckType.init(check_type="parameter_match")
>>> my_jmspath = "result[*].interfaces.*.[$name$,interfaceStatus,autoNegotiate]"
>>> post_value = my_check.get_value(output=post_data, path=my_jmspath)
>>> # mode: match - Match in the ouptut what is defined under 'params'
>>> my_parameter_match = {"mode": "match", "params": {"interfaceStatus": "connected", "autoNegotiate": "success"}}
>>> actual_results = my_check.evaluate(post_value, **my_parameter_match)
>>> actual_results
({'Management1': {'interfaceStatus': 'down'}}, False)
>>> # mode: no-match - Return what does nto match in the ouptut as defined under 'params'
>>> my_parameter_match = {"mode": "no-match", "params": {"interfaceStatus": "connected", "autoNegotiate": "success"}}
>>> actual_results = my_check.evaluate(post_value, **my_parameter_match)
>>> actual_results
({'Management1': {'autoNegotiate': 'success'}}, False
```

| Przemek: Why use dict unpacking when passing arguments to `evaluate`?

In network data, this could be a state of bgp neighbors being Established or the connectedness of certain interfaces being up.

| Przemek: This sentence should be moved above the example.

### Regex

The `regex` check type evaluates data against a regular expression passed as an argument to the `evaluate` method. Similarly to `parameter_match` check, the `match` and `no-match` modes are supported.

Let's run an example where we want to check the `burnedInAddress` key has a string representing a MAC Address as value

```python
>>> data = {
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
>>> # Python regex for matching MAC Address string
>>> regex_args = {"regex": "(?:[0-9a-fA-F]:?){12}", "mode": "match"}
>>> path = "result[*].interfaces.*.[$name$,burnedInAddress]"
>>> check = CheckType.init(check_type="regex")
>>> value = check.get_value(output=data, path=path)
>>> value
[{'Management1': {'burnedInAddress': '08:00:27:e6:b2:f8'}}]
>>> result = check.evaluate(value, **regex_args)
>>> # The test is passed as the burnedInAddress value match our regex
>>> result
({}, True)
>>> # What if we want "no-match"?
>>> regex_args = {"regex": "(?:[0-9a-fA-F]:?){12}", "mode": "no-match"}
>>> result = check.evaluate(value, **regex_args)
>>> # Netcompare return the failing data as the regex match the value
>>> result
({'Management1': {'burnedInAddress': '08:00:27:e6:b2:f8'}}, False)
```

| Przemek: Why use dict unpacking when passing arguments to `evaluate`?

### Operator

Operator is a check which includes an array of different evaluation logic. Here a summary of the available options:

| Przemek: What does it mean "array of different evaluation logic"? Can I ask for multiple checks to be performed at the same time? How do I define logic that should be used in the check?

| Przemek: The below is not very readable? Indented sections are rendered as code blocks. I would suggest naming these groups "categories" or "groups" and explaing that each of the names is the name of the check that needs to be passed as the argument.

#### `in` operators


    1. is-in: Check if the specified element string value is included in a given list of strings.
          - is-in: ["down", "up"] 
            check if value is in list (down, up)  

    2. not-in: Check if the specified element string value is NOT included in a given list of strings.
           - not-in: ["down", "up"] 
             check if value is not in list (down, up) 

    3. in-range: Check if the value of a specified element is in the given numeric range.
            - in-range: [20, 70]
              check if value is in range between 20 and 70 

    4. not-range: Check if the value of a specified element is outside of a given numeric range.
              - not-range: [5 , 40]
                checks if value is not in range between 5 and 40

#### `bool` operators

    1. all-same: Check if all content values for the specified element are the same. It can also be used to compare all content values against another specified element.
           - all-same: flap-count
             checks if all values of node <flap-count> in given path is same or not.

#### `str` operators

    1. contains: determines if an element string value contains the provided test-string value.
           - contains: "underlay"
           checks if "underlay" is present in given data or not. 

    2. not-contains: determines if an element string value does not contain the provided test-string value.
           - not-contains: "overlay"
           checks if "overlay" is present in given node or not.

#### `int`, `float` operators

    1. is-gt: Check if the value of a specified element is greater than a given numeric value.
            - is-gt: 2
              checks if value should be greater than 2  

    2. is-lt: Check if the value of a specified element is lesser than a given numeric value.
            - is-lt: 55
              checks if value is lower than 55 or not.  


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
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup,vrf,state]"
>>> # "operator" checks requires "mode" argument - which specify the operator logic to apply - 
>>> # and "operator_data" required for the mode defined.
>>> check_args = {"params": {"mode": "all-same", "operator_data": True}}
>>> check = CheckType.init("operator")
>>> value = check.get_value(data, path)
>>> value
[{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Connected'}}, {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}]
>>> result = check.evaluate(value, check_args)
>>> # We are looking for peers that have the same peerGroup,vrf and state. If not, return those are not. 
>>> result
((False, [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE', 'vrf': 'default', 'state': 'Connected'}}, {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE', 'vrf': 'default', 'state': 'Idle'}}]), False)
```

Let's now look to an example for the `in` operator. Keeping the same `data` and class object as above:

```python
>>> check_args = {"params": {"mode": "is-in", "operator_data": [20, 40, 50]}}
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
>>> value = check.get_value(data, path)
>>> value
[{'7.7.7.7': {'prefixesReceived': 101}}, {'10.1.0.0': {'prefixesReceived': 50}}]
>>> # We are looking for prefixesReceived value in operator_data list.
>>> result = check.evaluate(value, check_args)
>>> result
((True, [{'10.1.0.0': {'prefixesReceived': 50}}]), False)
```

What about `str` operator?

```python
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,peerGroup]"
>>> check_args = {"params": {"mode": "contains", "operator_data": "EVPN"}}
>>> value = check.get_value(data, path)
>>> value
[{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE'}}, {'10.1.0.0': {'peerGroup': 'IPv4-UNDERLAY-SPINE'}}]
>>> result = check.evaluate(value, check_args)
>>> result
((True, [{'7.7.7.7': {'peerGroup': 'EVPN-OVERLAY-SPINE'}}]), False)
```

Can you guess what would ne the outcome for an `int`, `float` operator?

```python
>>> path = "result[0].vrfs.default.peerList[*].[$peerAddress$,prefixesReceived]"
>>> check_args = {"params": {"mode": "is-gt", "operator_data": 20}}
>>> value = check.get_value(data, path)
>>> value
[{'7.7.7.7': {'prefixesReceived': 101}}, {'10.1.0.0': {'prefixesReceived': 50}}]
>>> result = check.evaluate(value, check_args)
>>> result
((True, [{'7.7.7.7': {'prefixesReceived': 101}}, {'10.1.0.0': {'prefixesReceived': 50}}]), False)
```

See [test](./tests) folder for more examples.

