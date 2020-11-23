$graph:
- baseCommand: scombi-do
  arguments: ['--profile', 'sigma0_vv_db', --resolution, 'highest', '--red-band', 'sigma0_vv_db'] 
  hints:
    DockerRequirement:
      dockerPull: scombi:latest 
  class: CommandLineTool
  id: clt
  inputs:
    inp1:
      inputBinding:
        position: 1
        prefix: --red-channel-input
      type: Directory
    inp2:
      inputBinding:
        position: 2
        prefix: --aoi
      type: string?
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /Applications/miniforge3/envs/env_scombi_do/bin/:/opt/anaconda3/envs/env_scombi_do/bin/:/srv/conda/envs/env_scombi_do/bin/:/opt/anaconda/envs/env_scombi_do/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/scombi_do
    ResourceRequirement: {}
#  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: This workflow creates SAR raster
  id: scombi-do-sigma0-raster
  inputs:
    input_reference:
      doc: SAR calibrated product 
      label: SAR calibrated product
      type: Directory
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
  label: SAR raster
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      Directory
  steps:
    node_1:
      in:
        inp1: input_reference
        inp2: aoi
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
