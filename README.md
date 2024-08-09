# DroneResponse mathtools

This package provides geodesy math tools for DroneResponse.

## Installation

```bash
pip install git+ssh://git@github.com/DroneResponse/python-droneresponse-mathtools#egg=droneresponse-mathtools
```

During install, you might see this harmless error: `invalid command 'bdist_wheel'`. You can ignore it.

After installing `droneresponse-mathtools` make sure you also install the `egm96-5.pgm` file. This file holds the dataset for the Earth Gravitational Model from 1996. You must install the file where geographiclib expects to find it. The easiest way to do so is to run:

```bash
sudo geographiclib-get-geoids egm96-5
```

For more information about the `geographiclib-get-geoids` script, or for instructions to install the file manually see the [geographiclib documentation about installing the geoid datasets](https://geographiclib.sourceforge.io/html/geoid.html#geoidinst).

## Example

To use this package:

```python
from droneresponse_mathtools import Lla
white_field = Lla(41.714911, -86.242250, 0)
pendle_rd = white_field.move_ned(106, 0, 0)
```

## Development


To run all the tests run:

```bash
tox
```

Note, to combine the coverage data from all the tox environments run:

```bash
PYTEST_ADDOPTS=--cov-append tox
```

### Development Setup

A complete development environment isn't necessary most of the time.
This setup lets you test with multiple python interpreters.
It also lets you use helper tools like `pre-commit`, which automatically cleans the source code before commits.

To set up a complete development environment on Ubuntu, install python3.6, python3.7, python3.8, python3.9, pip and venv.

```bash
sudo apt update
sudo apt install --yes software-properties-common python3 python3-pip python3-venv python3-wheel python3-dev
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install --yes python3.6 python3.7 python3.9
```

Set up `bumpversion`

```bash
pip install bumpversion
```

### How to package
First you need to download the `egm96` data and save it to `src/droneresponse_mathtools/geoids/egm96-5.pgm`.

This bash snippet will download the `egm96` data, and save it to the right spot using docker.
```bash
docker build --target geoid-downloader -t geoid-downloader-image .
docker run -d --name temp_container geoid-downloader-image bash -c "while true; do sleep 1; done"
docker cp  temp_container:/usr/share/GeographicLib/geoids ./src/droneresponse_mathtools/
docker stop -t 1 temp_container
docker rm temp_container
```

Once you have the `egm96` data you can create the `.whl` file

```bash
python setup.py bdist_wheel
```

Then you can access the file in `./dist`