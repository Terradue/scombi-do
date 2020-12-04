# Raster

This CWL workflow takes a local STAC catalog to produce an RGB composite described as a local STAC catalog.

It relies on the common band names for selecting the bands for the RGB composite channels.

## Inputs

* `input_reference`: the folder containing the local STAC catalog
* `red-band`: the band common name to use for the RGB composition red channel - Mandatory
* `green-band`: the band common name to use for the RGB composition green channel - Mandatory
* `blue-band`: the band common name to use for the RGB composition blue channel - Mandatory
* `aoi`: the area of interest expressed as a WKT expression - Optional
* `color`: the color manipulation operations (see https://github.com/mapbox/rio-color) - Optional

Example:

```yaml
input_reference: {'class': 'Directory', 'path': '/Users/fbrito/Documents/scombi-do/docker_tmpxcy75c4k/'}
red-band: 'red'
green-band: 'green'
blue-band: 'blue'
aoi: 'POLYGON((136.707 -35.991,136.707 -35.804,137.071 -35.804,137.071 -35.991,136.707 -35.991))'
color: 'Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.45'
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
cwltool --no-container scombi-do-raster.cwl#scombi-do-raster scombi-do-raster.yml
``` 