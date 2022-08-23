# Library Architecture

| ![jdiff HLD](./images/hld.png) |
|:---:|
| **`jdiff` architecture** |

We use the `CheckType` factory class method `create` along with the specified check type to instantiate a concrete object of the specified `CheckType` class.

```python
CheckType.create("exact_match")
>>> <jdiff.check_types.ExactMatchType at 0x10a618e80>
```

- `exact_match`
- `tolerance`
- `parameter_match`
- `regex`
- `operator`


Next, define a JSON object as reference data, as well as a JMESPath expression to extract the values wanted and pass them to `extract_data_from_json` method. Be aware! `jdiff` works with a customized version of JMESPath. More on that [below](#customized-jmespath).

```python
bgp_reference_state = "./pre/bgp.json"
bgp_jmspath_exp =  "result[0].vrfs.default.peerList[*].[$peerAddress$,establishedTransitions]"
bgp_reference_value = check.extract_data_from_json(bgp_reference_state, bgp_jmspath_exp)
```

Once the pre-change values are extracted, we would need to evaluate them against our post-change value. In the case of check-type `exact_match`, our post value would be another JSON object:

```python
bgp_comparison_state = "./post/bgp.json"
bgp_comparison_value = check.extract_data_from_json(bgp_post_change, bgp_jmspath_exp)
```

Each check type expects different types of arguments based on how and what they are checking. For example: check type `tolerance` needs a `tolerance` argument, whereas `parameter_match` expects a dictionary.

Now that we have pre and post data, we use the `evaluate` method to compare them, which will return our evaluation result.

```python
results = check.evaluate(post_value, pre_value, **evaluate_args)
```

# Customized JMESPath

Since `jdiff` works with JSON objects as data inputs, JMESPath was the obvious choice for traversing the data and extracting the value(s) to compare. However, JMESPath has a limitation where context is lost for the values it collects, in other words, for each given value that JMESPath returns, we cannot be sure what key it was part of.

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
result[0].vrfs.default.peerList[*].state
```

...which will return

```python
["Idle", "Connected"]
```

How can we understand that `Idle` is relative to peer 7.7.7.7 and `Connected` to peer `10.1.0.0`? 
We could index the output, but that would require some post-processing of the data. For that reason, `jdiff` uses a customized version of JMESPath where it is possible to define a reference key for the value(s) wanted. The reference key must be within `$` sign anchors and defined in a list, together with the value(s):

```python
result[0].vrfs.default.peerList[*].[$peerAddress$,state]
```

That  would give us...

```python
{"7.7.7.7": ["Idle"], "10.1.0.0": ["Connected"]}

```
