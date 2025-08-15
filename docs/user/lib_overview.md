# Library Overview

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key-values.

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](architecture.md#customized-jmespath).
