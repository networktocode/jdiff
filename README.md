# jdiff

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key-values.

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](#customized-jmespath).

## Installation 

Install from PyPI:

```
pip install jdiff
```

## Use cases

`jdiff` has been developed around diffing and testing structured data returned from APIs and other Python modules and libraries (such as TextFSM). Our primary use case is the examination of structured data returned from networking devices. However, we found the library fits other use cases where structured data needs to be operated on, and is especially useful when working or dealing with data returned from APIs.

## Documentation

Documentation is hosted on Read the Docs at [jdiff Documentation](https://jdiff.readthedocs.io/).