# Taiwan Reservoir Data

`generate-reservoir-data.py` gathers data from the [open data from Taiwan](https://data.gov.tw/) . Mainly the daily operational statistics and the reservoir condition data.

`dashboard.py` is to leverage the data and provide structured data for READr's Taiwan Dashboard.

## Usage

1. To build the image, run
  `docker build --tag generate-reservoir-data .`
2. To run the docker image, run
  `docker run --rm generate-reservoir-data`
