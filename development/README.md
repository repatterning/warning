
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

Herein, `-p 8000:8000` maps the host port `8000` to container port `8000`: 8888 ascertains access to [Jupyter Lab](https://docs.docker.com/guides/jupyter/).  Note, the container's working environment,
i.e., -w, must be inline with this project's top directory.  Additionally,

* --rm: [automatically remove container](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the)
* -i: [interact](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di)
* -t: [tag](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your)
* -p: [publish the container's port/s to the host](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s)

<br>

Get the name of a running instance of ``uncertanty`` via:

```shell
docker ps --all
```

Never deploy a root container, study the production [Dockerfile](../Dockerfile); cf. remote [.devcontainer/Dockerfile](../.devcontainer/Dockerfile)

<br>

### Remote Development & Integrated Development Environments

An IDE (integrated development environment) is a helpful remote development tool.  The **IntelliJ
IDEA** set up involves connecting to a machine's Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker), the steps are

<br>

> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** {select the linux operating system}
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

<br>

**Visual Studio Code** has its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).


<br>
<br>


## Code Analysis

The GitHub Actions script [main.yml](../.github/workflows/main.yml) conducts code analysis within a Cloud GitHub Workspace.  Depending on the script, code analysis may occur `on push` to any repository branch, or `on push` to a specific branch.

The sections herein outline remote code analysis.

<br>

### pylint

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Analyse a directory via the command

```shell
python -m pylint --rcfile .pylintrc {directory}
```

The `.pylintrc` file of this template project has been **amended to adhere to team norms**, including

* Maximum number of characters on a single line.
  > max-line-length=127

* Maximum number of lines in a module.
  > max-module-lines=135


<br>


### pytest & pytest coverage

The directive patterns

```shell
python -m pytest tests/{directory.name}/...py
pytest --cov-report term-missing  --cov src/{directory.name}/...py tests/{directory.name}/...py
```

for test and test coverage, respectively.


<br>


### flake8

For code & complexity analysis.  A directive of the form

```bash
python -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics src/data
```

inspects issues in relation to logic (F7), syntax (Python E9, Flake F7), mathematical formulae symbols (F63), undefined variable names (F82).  Additionally

```shell
python -m flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics src/data
```

inspects complexity.


<br>
<br>


## References

Time Series Modelling & Analysis:

* [Time Formatting Codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
* [Partial Auto-correlation Plot](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc4463.htm)
* [Autocorrelation Plot](https://www.itl.nist.gov/div898/handbook/eda/section3/autocopl.htm): Investigate questions such as (From NIST)
  * Is an observation related to an adjacent observation?
  * Is an observation related to an observation twice-removed? (etc.)
  * Is the observed time series white noise?
  * Is the observed time series sinusoidal?
  * Is the observed time series autoregressive?
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
* [Stationarity](https://otexts.com/fpp2/stationarity.html)
* [Stationarity, Detrending, Tests](https://www.statsmodels.org/dev/examples/notebooks/generated/stationarity_detrending_adf_kpss.html)
* [Model Identification for Southern Oscillations Data](https://www.itl.nist.gov/div898/handbook/pmc/section4/pmc4461.htm)
* [Robust detrending, rereferencing, outlier detection, and inpainting for multichannel data](https://pmc.ncbi.nlm.nih.gov/articles/PMC5915520/)
* [Using ARIMA and ETS models for forecasting water level changes for sustainable environmental management](https://www.nature.com/articles/s41598-024-73405-9)
* [Natural Logarithm Transformations](https://www.bridgetext.com/log-transforming-time-series-data-in-r)
* [Statistical forecasting: notes on regression and time series analysis](https://people.duke.edu/~rnau/411home.htm)
  * [Identifying the order of differencing in an ARIMA model](https://people.duke.edu/~rnau/411arim2.htm)
  * [Identifying the numbers of AR or MA terms in an ARIMA model](https://people.duke.edu/~rnau/411arim3.htm)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
