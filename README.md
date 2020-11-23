# scombi-do - Band combination

This step combines three bands as an RGB composite

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


