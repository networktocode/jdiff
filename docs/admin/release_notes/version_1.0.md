# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updated the entire project to the new Network to Code development standards.
- Added a JSON data compliance utility to help reconstruct JSON from compliance results.
- Major features or milestones
- Changes to compatibility with Nautobot and/or other apps, libraries etc.

## [v1.0.0] - 2025-08-25

### Added

- [#130](https://github.com/networktocode/jdiff/issues/130) - Add the ability to reconstruct JSON blobs to perform JSON data compliance.
- [#134](https://github.com/networktocode/jdiff/issues/134) - Added documentation on the release checklist and process for the library.
- [#149](https://github.com/networktocode/jdiff/issues/149) - Add is-subset and is-subset-ci operator modes for list comparison.

### Fixed

- [#128](https://github.com/networktocode/jdiff/issues/128) - Fixed the development standards to use 2025 standards.
- [#123](https://github.com/networktocode/jdiff/issues/123) Fixed Tag filtering not working in job launch form.
- [#133](https://github.com/networktocode/jdiff/issues/133), [#136](https://github.com/networktocode/jdiff/issues/136) - Fix GitHub release failing in CI pipeline.
- [#140](https://github.com/networktocode/jdiff/issues/140) - Fix invoke volume path.
- [#141](https://github.com/networktocode/jdiff/issues/141) - Fix GitHub CI Publish failures.

### Documentation

- Fixed the section headers for portions of the documentation.

### Housekeeping

- [#141](https://github.com/networktocode/jdiff/issues/141) - Pep508 compliant deepdiff dependency specification.
- Add .cookiecutter.json file for drift management.
- Run drift manager to update library.