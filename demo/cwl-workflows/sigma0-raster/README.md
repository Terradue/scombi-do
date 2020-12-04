# SAR Raster

This CWL workflow takes a local STAC catalog to produce an 8 byte image out of a calibrated SAR product.

## Inputs

* `input_reference`: the folder containing the local STAC catalog with an item including a 'sigma0_vv_db' asset
* `aoi`: the area of interest expressed as a WKT expression - Optional

Example:

```yaml
input_reference: {'class': 'Directory', 'path': '/Users/fbrito/Documents/scombi-do/docker_tmpxcy75c4k/'}
aoi: 'POLYGON((136.707 -35.991,136.707 -35.804,137.071 -35.804,137.071 -35.991,136.707 -35.991))'
```

## Execution 

### Requirements

You need `cwltool` to run the CWL document and `docker` to stage-in the input data. 

### Installation

Install this project with:

```console
git clone https://gitlab.com/charter-processing-environment/steps/scombi-do.git
cd scombi-do
```

Create the conda environment with

```console
conda env create -f environment.yml
```

Activate it with:

```console
conda activate env_scombi_do
```

Install the project with: 

```console
python setup.py install
```

Test the installation with:

```console
scombi-do --help
```

### Data stage-in

Use the stage-in as described in the project README.

Update the `scombi-do-raster.yml` file `input_reference` parameter with the staged path.

### Running

```console
cwltool --no-container scombi-do-raster.cwl#scombi-do-sigma0-raster scombi-do-sigma0-raster.yml
``` 