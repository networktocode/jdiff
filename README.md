# jdiff

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare--via key presense/absense and value comparison--JSON data objects

Our primary use case is the examination of structured data returned from networking devices, such as:

* Compare the operational state of network devices pre and post change
* Compare operational state of a device vs a "known healthy" state
* Compare state of similar devices, such as a pair of leafs or a pair of backbone routers
* Compare operational state of a component (interface, vrf, bgp peering, etc.) migrated from one device to another

However, the library fits other use cases where structured data needs to be operated on.

## Installation 

Install from PyPI:

```
pip install jdiff
```

## Intelligent Comparison

The library provides the ability to ask more intelligent questions of a given data structure. Comparisons of data such as "Is my pre change state the same as my post change state", is not that interesting of a comparison. The library intends to ask intelligent questions _like_:

* Is the route table within 10% of routes before and after a change?
* Is all of the interfaces that were up before the change, still up?
* Are there at least 10k sessions of traffic on my firewall?
* Is there there at least 2 interfaces up within lldp neighbors?

## Technical Overview

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](#customized-jmespath).

`jdiff` has been developed around diffing and testing structured data returned from Network APIs and libraries (such as TextFSM) but is equally useful when working or dealing with data returned from APIs.

## Documentation

Documentation is hosted on Read the Docs at [jdiff Documentation](https://jdiff.readthedocs.io/).
