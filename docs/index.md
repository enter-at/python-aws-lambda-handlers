# lambda-handlers

An opinionated Python package that facilitates specifying AWS Lambda handlers.

It includes input validation, error handling and response formatting.

## Install the latest

To install the latest version of lambda-handlers simply run:

```bash
pip install lambda-handlers
```

If you are going to use validation, you should choose between
[Marshmallow](https://pypi.org/project/marshmallow/) or
[jsonschema](https://pypi.org/project/jsonschema/).

To install with one of these:

```bash
pip install 'lambda-handlers[marshmallow]'
```

or

```bash
pip install 'lambda-handlers[jsonschema]'
```
