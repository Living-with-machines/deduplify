# Contributing to deduplify

:+1: :tada: First off, thank you for taking the time to contribute! :tada: :+1:

The following is set of guidelines for contributing to `deduplify` hosted on [GitHub](https://github.com/Living-with-machines/deduplify).
These are mostly guidelines, not rules.
Use your best judgment and feel free to propose changes to this document in a pull request.

**Table of Contents:**

- [Code of Conduct](#code-of-conduct)
- [I don't want to read the whole thing, I just have a question!](#i-dont-want-to-read-the-whole-thing-i-just-have-a-question)
- [How can I contribute?](#how-can-i-contribute)
  - [Reporting bugs and/or missing features](#reporting-bugs-andor-missing-features)
  - [Pull Requests](#pull-requests)
  - [Making a Release](#making-a-release)
- [Style Guides](#style-guides)
  - [Python Style Guide](#python-style-guide)

---

## Code of Conduct

This project and everyone participating in it is governed by the project's [Code of Conduct](./CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behaviour to [sgibson@turing.ac.uk](mailto:sgibson@turing.ac.uk).

## I don't want to read the whole thing, I just have a question!

Please [open an issue](https://github.com/Living-with-machines/deduplify/issues/new/choose) and we'll try to help you as soon as possible.

## How can I contribute?

### Reporting bugs and/or missing features

We believe it's actually really difficult to tell if something not working is due to a bug or if there's something missing in the code that allows users to do something.
Therefore, we don't have `bug` and `enhancement` labels/issue templates.
Instead we have a `support` template that asks for details of what a user expected to happen.
We can then begin a discussion from there as to whether this requires a bugfix or a feature release.

If you think you've found something missing or broken within `deduplify`, please [open a support issue](https://github.com/Living-with-machines/deduplify/issues/new?assignees=&labels=needs%3A+triage&template=support.md&title=) and we will try to help find a solution.
Please try to complete the template to the best of your ability with as much detail as possible.
This will help us work out what's happening and what needs to be done.

### Pull Requests

If you find or file an issue in the project that you would like to work on, here are the steps to take:

1. Please add a comment on the issue stating you would like to work on it. This reduces the chance of duplicated work.
2. Work on any changes in a fork of this repository.
3. When you open your Pull Request, please complete the PR template to the best of your ability.
4. Please try to maintain passing status checks on your Pull Request. However, the project team can help with tricky test failures.

### Making a Release

We use a package called [`incremental`](https://github.com/twisted/incremental) to simplify the changing the [semantic version](https://semver.org/) of the package.
A [GitHub Action workflow](https://github.com/Living-with-machines/deduplify/blob/HEAD/.github/workflows/pypi.yml) is configured to build and publish the package on [PyPI](https://pypi.org/project/deduplify/) when a new release is published.

To make a release, follow these steps:

1. Bump the package version using `incremental`.
   Add and commit the edited `_version.py` file in the `deduplify` folder.
   This can either be done as a commit in a larger Pull Request, or in a PR by itself.
   - To increase the patch of the version, run:
     ```bash
     python -m incremental.update --patch deduplify
     ```
   - To increase either the major or minor tag of the version, run:
     ```bash
     python -m incremental.update --newversion X.Y.Z deduplify
     ```
     where `X.Y.Z` matches a valid SEMVAR version number.
2. In the GitHub browser, make a new release tag.
   - Click the `Releases` tab at the top of the repository
   - Click the `Draft a new release` button
   - In the `Choose a tag` dropdown menu, type your new version with a leading `v`, e.g., `vX.Y.Z`.
     This tag won't exist yet, so select `Create new tag on publish`.
   - Click `Auto-generate release notes` to automatically generate the release notes
   - Click `Publish release`
## Style Guides

### Python Style Guide

`deduplify` is a Python package and we try to maintain certain formatting standards for readability and consistency, but also that _you_ don't have to worry about the style either!

All Python files within this project are run through [`black`](https://github.com/psf/black), [`flake8`](https://flake8.pycqa.org/en/latest/), [`pyupgrade`](https://github.com/asottile/pyupgrade) and [`isort`](https://pycqa.github.io/isort/) for formatting and linting using [`pre-commit`](https://pre-commit.ci).
`pre-commit` will automatically apply the required changes to all Python files in order to ensure they conform to the style guide.
You can see the [`pre-commit` config file](https://github.com/Living-with-machines/deduplify/blob/HEAD/.pre-commit-config.yaml) in the repository.
