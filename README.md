# netcompare

This library is meant to be a light-weight way to compare structured output from network device `show` commands. `netcompare` is a python library targeted at intelligently deep diffing structured data objects of json type. In addition, `netcompare` provides some basic tests of keys and values within the data structure.

The libraly heavely rely on [jmspath](https://jmespath.org/) for traversing the json object and find the wanted value to be evaluated. More on that later.

## Use Case

`netcompare` enables an easy and direct way to see the outcome of network configuration or operational status change. The intended usage is to collect structured `show` command output before and after a change window. Prior to closing the change window, the results are compared to help determine if the change was successful as intended and if the network is in an acceptable state. The output can be stored with the change's documentation for easy reference and proof of completion.

## Library Architecture

![netcompare HLD](./docs/images/hld.png)

As first thing, an instance of `CheckType` object must be created passing one of the below check types as argument:

- `exact_match`
- `tolerance`
- `parameters`
- `regex`
- `operator`


```python
my_check = "exact_match"
check = CheckType.init(my_check)
```

We would then need to define our json object used as reference data, as well as a JMSPATH expression to extract the value wanted and pass them to `get_value` method. Be aware! `netcompare` works with a customized version of JMSPATH. More on that later.

```python
bgp_pre_change = "./pre/bgp.json"
bgp_jmspath_exp =  "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]"
pre_value = check.get_value(bgp_pre_change, bgp_jmspath_exp)
```

Once extracted our pre-change value, we would need to evaluate it against our post-change value. In case of chec-type `exact_match` our post-value would be another json object:

```python
bgp_post_change = "./post/bgp.json"
post_value = check.get_value(bgp_post_change, bgp_jmspath_exp)
```

Every check type expect different type of arguments. For example, in case of check type `tolerance` we would also need to pass `tolerance` argument; `parameters` expect only a dictionary...

Now that we have pre and post data, we just need to compare them with `evaluate` method which will return our evaluation result.

```python
results = check.evaluate(post_value, pre_value, **evaluate_args)
```

## Customized JMSPATH

Since `netcompare` work with json object as data inputs, JMSPATH was the obvous choise for traversing the data and extract the value wanted from it.

However, JMSPATH comes with a limitation where is not possible to define a `key` to which the `value` belongs to.

Let's have a look to the below `show bgp` output example.

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
If we would define a JMSPATH expression to extract `state` we would have something like...

```python
"result[0].vrfs.default.peerList[*].state
```

...which will return

```python
["Idle", "Connected"]
```

How can we understand that `Idle` is relative to peer 7.7.7.7 and `Connected` to peer `10.1.0.0` ? 
We could index the output but that would require some post-processing data. For that reason, `netcompare` use a customized version of JMSPATH where is possible to define a reference key for the value(s) wanted. The reference key must be within `$` sign anchors and defined in a list, together with the value(s):

```python
"result[0].vrfs.default.peerList[*].[$peerAddress$,state]
```

That  would give us...

```python
{"7.7.7.7": ["Idle"], "10.1.0.0": ["Connected"]}

```

## Check types explained

### exact_match

Check type `exact_match` is concerned about the value of the elements within the data structure. The keys and values should match between the pre and post values. A diff is generated between the two data sets. 
As some outputs might be too verbose or includes fields that constantly change (i.e. interface counter), is possible to exclude a portion of data traversed by JMSPATH, defining a list of keys that we want to exclude.

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

As we can see, we return a tuple containing a diff betwee the pre and post data as well as a boolean for the overall test result. In this case a diff has been found so the status of the test is `False`.

Let's see a better way to run `exact_match` for this specific case. Since we are interested only into `interfaceStatus` we could write our JMSPATH expression as:

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
Targeting only `interfaceStatus` key, we would need to define a reference key (in this case `$name$`) as well as we would not need to define any exclusion list. 

The anchor logic for reference key applies to all check-types available in `netcompare`


### parameter_match

parameter_match provides a way to match keys and values in the output with known good values. 

The test defines key/value pairs known to be the good value - type `dict()` - as well as a mode - `match`, `no-match` - to match or not against the parsed output. The test fails if any status has changed based on what is defined in pre/post. If there are new values not contained in the input/test value, that will not count as a failure.


Examples:

```python
>>> from netcompare import CheckType
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
>>> post_value = my_check.get_value(output=pre_data, path=my_jmspath)
>>> my_parameter_match = {"mode": "match", "params": {"interfaceStatus": "connected", "autoNegotiate": "success"}}
>>> my_parameter_match = {"mode": "match", "params": {"interfaceStatus": "connected", "autoNegotiate": "success"}}
>>> actual_results = my_check.evaluate(post_value, **my_parameter_match)
>>> actual_result
({}, True)
```

In network data, this could be a state of bgp neighbors being Established or the connectedness of certain interfaces being up.

### Tolerance

The `tolerance` test defines a percentage of differing `float()` between the pre and post checks. The threshold is defined as a percentage that can be different either from the value stated in pre and post fields. 

The threshold must be `float > 0`, is percentge based, and will be counted as a range centered on the value in pre and post.

```
Pre: 100 
Post: 110
Threshold: 10
-----------------
PASS/PASS
Pre:  [100]
Post: [110]

PASS/PASS
Pre:  [100]
Post: [120]

PASS/PASS
Pre:  [100]
Post: [100]

PASS/FAIL
Pre:  [100]
Post: [90]

PASS/FAIL
Pre:  [90]
Post: [20]

FAIL/FAIL
Pre:  [80]
Post: [120]
```

This test can test the tolerance for changing quantities of certain things such as routes, or L2 or L3 neighbors. It could also test actual outputted values such as transmitted light levels for optics.

## How To Define A Check

The check requires at least 2 arguments: `check_type` which can be `exact_match`, `tolerance`, `parameter_match` or `path`. The `path` argument is JMESPath based but uses `$` to anchor the reference key needed to generate the diff - more on this later. 

Example #1:

Run an `exact_match` between 2 files where `peerAddress` is the reference key (note the anchors used - `$` ) for `statebgpPeerCaps`. In this example, key and value are at the same level.

Check Definition:
```
{
  "check_type": "exact_match",
  "path": "result[0].vrfs.default.peerList[*].[$peerAddress$,statebgpPeerCaps]",
}
```

Show Command Output - Pre:
```
{
  "jsonrpc": "2.0",
  "id": "EapiExplorer-1",
  "result": [
    {
      "vrfs": {
        "default": {
          "peerList": [
            {
              "linkType": "external",
              "localAsn": "65130.1100",
              "prefixesSent": 52,
              "receivedUpdates": 0,
              "peerAddress": "7.7.7.7",
              "v6PrefixesSent": 0,
              "establishedTransitions": 0,
              "bgpPeerCaps": 75759616,
              "negotiatedVersion": 0,
              "sentUpdates": 0,
              "v4SrTePrefixesSent": 0,
              "lastEvent": "NoEvent",
              "configuredKeepaliveTime": 5,
              "ttl": 2,
              "state": "Idle",
              ...
```
Show Command Output - Post:
```
{
  "jsonrpc": "2.0",
  "id": "EapiExplorer-1",
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
              "v6PrefixesSent": 0,
              "establishedTransitions": 0,
              "bgpPeerCaps": 75759616,
              "negotiatedVersion": 0,
              "sentUpdates": 0,
              "v4SrTePrefixesSent": 0,
              "lastEvent": "NoEvent",
              "configuredKeepaliveTime": 5,
              "ttl": 2,
              "state": "Connected",
```

Result:
```
{
    "7.7.7.7": {
        "state": {
            "new_value": "Connected",
            "old_value": "Idle"
        }
    }
}
```
`result[0].vrfs.default.peerList[*].$peerAddress$` is the reference key (`7.7.7.7`) that we want associated to our value used to generate diff (`state`)...otherwise, how can we understand which `statebgpPeerCaps` is associated to which `peerAddress` ?

Example #2:

Similar to Example 1 but with key and value on different level. In this example `peers` will be our reference key, `accepted_prefixes` and `received_prefixes` the values used to generate diff.

Check Definition:
```
{
  "check_type": "exact_match",
  "path": "global.$peers$.*.*.ipv4.[accepted_prefixes,received_prefixes]",
}
```

Show Command Output - Pre:
```
{
    "global": {
        "peers": {
            "10.1.0.0": {
                "address_family": {
                    "ipv4": {
                        "accepted_prefixes": -9,
                        "received_prefixes": 0,
                        "sent_prefixes": 0
                    },
                    ....
```

Show Command Output - Post:
```
{
    "global": {
        "peers": {
            "10.1.0.0": {
                "address_family": {
                    "ipv4": {
                        "accepted_prefixes": -1,
                        "received_prefixes": 0,
                        "sent_prefixes": 0
                        ...
```

Result:
```
{
    "10.1.0.0": {
        "accepted_prefixes": {
            "new_value": -1,
            "old_value": -9
        }
    },
    ...
```

Example #3:

Similar to Example 1 and 2 but without a reference key defined in `path`, plus some excluded fields to remove verbosity from diff output

Check Definition:
```
{
  "check_type": "exact_match", 
  "path": "result[*]", 
  "exclude": ["interfaceStatistics", "interfaceCounters"],
}
```

Show Command Output - Pre:
```
{
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
            },
            ...
```

Show Command Output - Post:
```
{
    "jsonrpc": "2.0",
    "id": "EapiExplorer-1",
    "result": [
      {
        "interfaces": {
          "Management1": {
            "lastStatusChangeTimestamp": 1626247821.123456,
            "lanes": 0,
            "name": "Management1",
            "interfaceStatus": "connected",
            "autoNegotiate": "success",
            "burnedInAddress": "08:00:27:e6:b2:f8",
            "loopbackMode": "loopbackNone",
            "interfaceStatistics": {
              "inBitsRate": 3403.4362520883615,
              "inPktsRate": 3.7424095978179257,
              "outBitsRate": 16249.69114419833,
              "updateInterval": 300,
              "outPktsRate": 2.1111866059750692
            },
          ...
```

Result:

```
{
  "interfaces": {
      "Management1": {
          "lastStatusChangeTimestamp": {
              "new_value": 1626247821.123456,
              "old_value": 1626247820.0720868
          },
          "interfaceAddress": {
              "primaryIp": {
                  "address": {
                      "new_value": "10.2.2.15",
                      "old_value": "10.0.2.15"
                  }
              }
          }
      }
  }
}
```

See [test](./tests) folder for more examples.

