# jdiff

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key values.

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](#customized-jmespath).

## Getting started


First you import the CheckType class.

```python
from jdiff import CheckType
```

Get (or fabricate) some data (this data may also be loaded from a file or from a string, more examples later).

```python
a = {"foo": "bar"}
b = {"foo": "bar baz"}
```

Call the `create` method of the `CheckType` class to get an instance of the check type you want to perform.

```python
match = CheckType.create("exact_match")
```

Evaluate the check type and the diff.
```python
match.evaluate(a, b)
>>> ({'foo': {'new_value': 'bar baz', 'old_value': 'bar'}}, False)
```

This results in a tuple:
- The first value is the diff between the two data structures
- The second value is a boolean with the result of the check

This diff can also show if any keys were added or deleted. 
The second value returned will be the boolean result of the check. In this case, the two data structures were not an exact match.

| Stephen - we may want to remove these next two paragraphs
For instance, the reference state can be collected from the network directly using any method that returns structured data: Ansible, NAPALM, Nornir to name a few. You could also choose to generate the reference state from an SoT, such as [Nautobot](https://github.com/nautobot/nautobot/), and have a true intended state.

`jdiff` is perfectly suited to work with data gathered from network devices via show commands, Ansible playbooks, as well as in applications such as [Nautobot](https://github.com/nautobot/nautobot/), or [Netbox](https://github.com/netbox-community/netbox). `jdiff` is focused on being the 'plumbing' behind a full network automation validation solution.

## Checking data structures

As shown in the example, the check evaluation both performs a diff and tests the objects. All of the concrete `CheckTypes` both perform the diff and their specified check.

More on the **check** part: the check provides a way to test some keys or values in our collected data. The check portion is focused on providing a boolean result of the test. There are a few different ways to check our data. 

These are the different checks that can be performed on the data. These both describe the type of check and are also used as the argument to instantiate that type of check with the create method: `CheckType.create("check_type")`.

- `exact_match`: the keys and values must match exactly between the two objects
- `tolerance`: the keys must match and the values can differ according to the 'tolerance' value provided
- `parameter_match`: a reference key and value is provided and its presence (or absence) is checked in the provided object
- `regex`: a reference regex pattern is provided which is used to find a match in the provided object
- `operator`: similar to parameter match, but the reference includes several different possible operators: 'in', 'bool', 'string', and numerical comparison with 'int' and 'float' to check against

`CheckTypes` are explained in more detail in the [CheckTypes Explained section](#check-types-explained).


## Workflow

| ![jdiff workflow](./docs/images/workflow.png) |
|:---:|
| **`jdiff` workflow** |

| Przemek: I think this diagram would work better if it were wide, rather than tall. Netcompare name should match the name we choose for this library (e.g. Netcompare instead of NETCOMPARE). The individual Netcompare components are difficult to read in the vertical orientation.


1. The reference state object is retrieved or assembled. The structured data may be from:

    - an API
    - another Python module/library
    - retrieved from a saved file
    - constructed programmatically

2. Some time passes where some change to the data may occurr.
3. The comparison state is retrieved or assembled, often using a similar process used to get the reference state.
4. The reference state is then compared to the current state using the jdiff library.