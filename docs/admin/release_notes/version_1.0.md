# v1.0 Release Notes

This document describes all new features and changes in the release `1.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updated the entire project to the new Network to Code development standards.
- Added a JSON data compliance utility to help reconstruct JSON from compliance results.
- Major features or milestones
- Changes to compatibility with Nautobot and/or other apps, libraries etc.

## [v1.0.2] - 2026-03-23

### Added

- [#149](https://github.com/networktocode/jdiff/issues/149) - Add is-subset and is-subset-ci operator modes for list comparison.

### Fixed

- [#140](https://github.com/networktocode/jdiff/issues/140) - Fix invoke volume path.
- [#142](https://github.com/networktocode/jdiff/issues/142) - Fix GitHub CI Publish failures.

### Documentation

- Fixed the section headers for portions of the documentation.

### Housekeeping

- [#142](https://github.com/networktocode/jdiff/issues/142) - Pep508 compliant deepdiff dependency specification.
- Add .cookiecutter.json file for drift management.
- Run drift manager to update library.

## [v1.0.1] - 2025-09-04

### Added

- [#134](https://github.com/networktocode/jdiff/issues/134) - Added documentation on the release checklist and process for the library.

### Fixed

- [#133](https://github.com/networktocode/jdiff/issues/133) - Update DeepDiif dependency to 8.6.1
- [#136](https://github.com/networktocode/jdiff/issues/136) - Update DeepDiif dependency to 8.6.1

## [v1.0.0] - 2025-08-25

### Added

- [#130](https://github.com/networktocode/jdiff/issues/130) - Add the ability to reconstruct JSON blobs to perform JSON data compliance.

### Fixed

- [#128](https://github.com/networktocode/jdiff/issues/128) - Fixed the development standards to use 2025 standards.
- [#123](https://github.com/networktocode/jdiff/issues/123) - Fixed Tag filtering not working in job launch form.
