
<br>

## Environments

### Remote Development

For this Python project/template, the remote development environment requires

* [Dockerfile](../.devcontainer/Dockerfile)
* [requirements.txt](../.devcontainer/requirements.txt)

An image is built via the command

```shell
docker build . --file .devcontainer/Dockerfile -t uncertainty
```

On success, the output of

```shell
docker images
```

should include

<br>

| repository   | tag    | image id | created  | size     |
|:-------------|:-------|:---------|:---------|:---------|
| uncertainty  | latest | $\ldots$ | $\ldots$ | $\ldots$ |


<br>

Subsequently, run a container, i.e., an instance, of the image `uncertainty` via:

<br>

```shell
docker run --rm -i -t -p 8000:8000 -p 8888:8888 -w /app --mount
    type=bind,src="$(pwd)",target=/app uncertainty
```

or

```shell
docker run --rm -i -t -p 8000:8000 -p 8888:8888 -w /app --mount
    type=bind,src="$(pwd)",target=/app 
    -v ~/.aws:/root/.aws uncertainty
```


<br>

<br>
<br>


## References

Time Series Modelling & Analysis:

* [Time Formatting Codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
* [Partial Auto-correlation Plot](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc4463.htm)
* [statsmodels.tsa.stattools.pacf](https://www.statsmodels.org/dev/generated/statsmodels.tsa.stattools.pacf.html)
* [statsmodels.graphics.tsaplots.plot_pacf](https://www.statsmodels.org/dev/generated/statsmodels.graphics.tsaplots.plot_pacf.html)

<br>

<abbr title="Scottish Environment Protection Agency">SEPA</abbr>:
* [Application Programming Interface](https://timeseriesdoc.sepa.org.uk/api-documentation/)
* [Query Service](https://timeseries.sepa.org.uk/KiWIS/KiWIS?datasource=0&service=kisters&type=queryServices&request=getrequestinfo)
* [Water Levels](https://www.sepa.org.uk/environment/water/water-levels/)
  * [Water Levels](https://waterlevels.sepa.org.uk/)
* [Catchment boundaries for Scotland based on Scottish Environment Protection Agency (SEPA) catchments (WGS84) 2023](https://data.cefas.co.uk/view/21970)
* [Environmental Data](https://www.sepa.org.uk/environment/environmental-data/)
* [Geospatial Standards Register](https://www.gov.uk/government/publications/uk-geospatial-data-standards-register/national-geospatial-data-standards-register)
* [Access Control](https://timeseriesdoc.sepa.org.uk/api-documentation/before-you-start/what-controls-there-are-on-access/)
* [Quality Codes](https://timeseriesdoc.sepa.org.uk/api-documentation/before-you-start/how-data-validity-may-change/)

<br>

Extra:
* [Gauge Height](https://waterdata.usgs.gov/blog/gage_height/)
* [python: hub.docker.com](https://hub.docker.com/_/python/)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
