# qiskit-benchmark

![Python 3](https://img.shields.io/badge/python-3-blue?logo=python)
[![License](https://img.shields.io/badge/license-MIT-green)](https://choosealicense.com/licenses/mit/)
[![Code style](https://img.shields.io/badge/style-black-black)](https://pypi.org/project/black)

A simple qiskit benchmark that runs random circuits and measures the time
taken. Produces a CSV file and pretty heatmap plots.

## Dependencies

- `python3.10` or newer;
- python packages listed `requirements.txt`

## Usage

```sh
python3.10 -m qiskit_benchmark output/dir/path [options...]
```

Run `python3.10 -m qiskit_benchmark --help` to see the list of available
options.

## Contributing

### Dependencies

- `python3.10` or newer;
- `requirements.txt` for runtime dependencies;
- `requirements.dev.txt` for development dependencies.
- `make` (optional);

Simply run

```sh
virtualenv venv -p python3.10
. ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

### Documentation

Simply run

```sh
make docs
```

This will generate the HTML doc of the project, and the index file should be at
`docs/index.html`. To have it directly in your browser, run

```sh
make docs-browser
```

### Code quality

Don't forget to run

```sh
make
```

to format the code following [black](https://pypi.org/project/black/),
typecheck it using [mypy](http://mypy-lang.org/), and check it against coding
standards using [pylint](https://pylint.org/).
