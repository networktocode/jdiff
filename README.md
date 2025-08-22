# Jdiff

<p align="center">
  <img src="https://raw.githubusercontent.com/networktocode/jdiff/develop/docs/images/jdiff_logo.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/networktocode/jdiff/actions"><img src="https://github.com/networktocode/jdiff/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://jdiff.readthedocs.io/en/latest"><img src="https://readthedocs.org/projects/jdiff/badge/"></a>
  <a href="https://pypi.org/project/jdiff/"><img src="https://img.shields.io/pypi/v/jdiff"></a>
  <a href="https://pypi.org/project/jdiff/"><img src="https://img.shields.io/pypi/dm/jdiff"></a>
  <br>
</p>

## Overview

`jdiff` is a lightweight Python library allowing you to examine structured data. `jdiff` provides an interface to intelligently compare JSON data objects and test for the presence (or absence) of keys. You can also examine and compare corresponding key-values.

## Documentation

Full web-based HTML documentation for this library can be found over on the [Jdiff Docs](https://jdiff.readthedocs.io) website:

- [User Guide](https://jdiff.readthedocs.io/en/latest/user/lib_overview/) - Overview, Using the library, Getting Started.
- [Administrator Guide](https://jdiff.readthedocs.io/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the library.
- [Developer Guide](https://jdiff.readthedocs.io/en/latest/dev/contributing/) - Extending the library, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://jdiff.readthedocs.io/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://jdiff.readthedocs.io/en/latest/user/faq/).

### Contributing to the Docs

All the Markdown source for the library documentation can be found under the [docs](https://github.com/networktocode/jdiff/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.

If you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://jdiff.readthedocs.io/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://jdiff.readthedocs.io/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#networktocode`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
