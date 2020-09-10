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
- [Styleguides](#styleguides)
  - [Python Styleguide](#python-styleguide)

---

### Code of Conduct

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

## Styleguides

### Python Styleguide

`deduplify` is a Python package and we try to maintain certain formatting standards for readability and consistency, but also that _you_ don't have to worry about the style either!

All Python files within this project are run through [`black`](https://github.com/psf/black) and [`flake8`](https://flake8.pycqa.org/en/latest/) for formatting and linting checks as part of our CI workflow.
While not conforming to these standards won't block a contributing, we really recommend sticking with them for the hygiene of the project.
