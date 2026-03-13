# Library Overview

This document provides an overview of the library including critical information and important considerations.

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key-values.

## Description

The library heavily relies on [JMESPath](https://jmespath.org/) for traversing the JSON object and finding the values to be evaluated. More on that [here](architecture.md#customized-jmespath).

## Audience (User Personas) - Who should use this Library?

The intended audience is those who are programming with Python and specifically with JSON encoded data. Whether you are a seasoned veteran or a casual scripter, this library should help to reduce duplication between various reinventing the wheel.

## Authors and Maintainers

- @lvrfrc87
- @scetron
- @grelleum
- @jeffkala
- @pszulczewski
