# scombi-do - Band combination

This step combines input bands with optional band arithmetic to produce an RGB composite.

## Try on binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Terradue/scombi-do/HEAD?urlpath=lab&filepath=demo%2Fscombi-do-demo.ipynb)

## Concept

### Output channel content manipulation

The output content is driven by input data manipulation using s expressions (see Mapbox/snuggs) to define numpy operations as a series of operations provided as strings.

The result of these manipulations target producing an array with values in the [0,1] interval

The example below takes the reflectances encoded as Int16 with a scaling factor of 0.0001 and converts it to [0,1]:

```yaml
- '(interp v1 (asarray 0 10000) (asarray 0 1))'
- '(interp v2 (asarray 0 10000) (asarray 0 1))'
- '(interp v3 (asarray 0 10000) (asarray 0 1))'
```

Instead the other example below does an amplitude change RGB composite clipping the sigma0 encoded as db:

```yaml
- '(interp v1 (asarray -15 5) (asarray 0 1))'
- '(interp v1 (asarray -15 5) (asarray 0 1))'
- '(interp v2 (asarray -15 5) (asarray 0 1))'
```

v1, v2 and v3 are the numpy arrays extracted from the inputs received.

### Color manipulation

The color manipulation uses rio_color (link to rio_color) to enhance the RGB composite. 

An example of such a color manipulation is: `'Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.35'`

### Using pre-defined configurations

There are a number of pre-defined profiles that cover a set of typicall needs.

The profiles are defined in a YAML file.

An example of such a file is:

```yaml
profiles:
    'composite':
       band_count: 3
       color: 'Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.35' 
       expression: 
         - '(interp v1 (asarray 0 10000) (asarray 0 1))'
         - '(interp v2 (asarray 0 10000) (asarray 0 1))'
         - '(interp v3 (asarray 0 10000) (asarray 0 1))'
    'normalized_difference':
       band_count: 2
       expression:
         - '(interp (/ (- v1 v2) (+ v1 v2)) (asarray -1 1) (asarray 0 1))'
```

#### Composite profile

The `composite` profile is defined as:

```yaml
'composite':
       band_count: 3
       color: 'Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.35' 
       expression: 
         - '(interp v1 (asarray 0 10000) (asarray 0 1))'
         - '(interp v2 (asarray 0 10000) (asarray 0 1))'
         - '(interp v3 (asarray 0 10000) (asarray 0 1))'
```

This profile takes three inputs, one for each RGB channel and:
- does an interpolation between [0,10000] to [0,1].
- applies the rio_color expression 'Gamma RGB 3.5 Saturation 1.4 Sigmoidal RGB 15 0.35' 

#### Normalized difference

```yaml
    'normalized_difference':
       band_count: 2
       expression:
         - '(interp (/ (- v1 v2) (+ v1 v2)) (asarray -1 1) (asarray 0 1))'
```


## Development 

```bash
cd scombi_do
```

```bash
conda env create -f environment.yml
```

Activate the conda environment

```bash
conda activate  env_scombi_do
```

To build and install the project locally:

```
python setup.py install
```

Test the CLI with:

```bash
scombi-do --help
```

## Building the docker image

Build the docker image with:

```bash
docker build -t scombi_do:0.1  -f .docker/Dockerfile .
```

or for pushing to the `terradue` docker repository:

```bash
docker build -t terradue/scombi_do:0.1  -f .docker/Dockerfile .
```

Test the CLI with:

```bash
docker run --rm -it scombi_do:0.1 scombi-do --help
```

or 

```bash
docker run --rm -it terradue/scombi_do:0.1 scombi-do --help
```

## Data stage-in

Use the `stage-in.cwl` document provided to stage three Sentinel-2 acquisitions:

```console
cwltool stage-in.cwl stage-in.yml
```

Use the folders returned by the execution as parameters when using `scombi-do` 

## scombi-do introduction


