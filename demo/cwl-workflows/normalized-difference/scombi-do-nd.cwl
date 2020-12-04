$graph:
- baseCommand: scombi-do
  arguments: ['--profile', 'normalized_difference', --resolution, 'highest'] 
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
        prefix: --green-channel-input
      type: Directory
    inp3:
      inputBinding:
        position: 3
        prefix: --red-band
      type: string
    inp4:
      inputBinding:
        position: 4
        prefix: --green-band
      type: string
    inp5:
      inputBinding:
        position: 5
        prefix: --aoi
      type: string?
    inp6:
      inputBinding:
        position: 6
        prefix: --lut
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
  doc: This workflow creates an RGB combination 
  id: scombi-do-nd
  inputs:
    input_reference_1:
      doc: EO product 
      label: EO product 
      type: Directory
    input_reference_2:
      doc: EO product 
      label: EO product 
      type: Directory
    band_1:
      doc: Common band name for normalized difference 
      label: Common band name for normalized difference 
      type: string
    band_2:
      doc: Common band name for normalized difference 
      label: Common band name for normalized difference 
      type: string
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
    lut:
      doc: Look-up table
      label: Look-up table
      type: string?
  label: RGB combination 
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      Directory
  steps:
    node_1:
      in:
        inp1: input_reference_1
        inp2: input_reference_2
        inp3: band_1
        inp4: band_2
        inp5: aoi
        inp6: lut
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
