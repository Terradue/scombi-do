$graph:
- baseCommand: scombi-do
  arguments: ['--profile', 'composite', --resolution, 'highest'] 
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
      type: Directory?
    inp3:
      inputBinding:
        position: 3
        prefix: --blue-channel-input
      type: Directory?
    inp4:
      inputBinding:
        position: 4
        prefix: --red-band
      type: string
    inp5:
      inputBinding:
        position: 5
        prefix: --green-band
      type: string?
    inp6:
      inputBinding:
        position: 6
        prefix: --blue-band
      type: string?
    inp7:
      inputBinding:
        position: 7
        prefix: --aoi
      type: string?
    inp8:
      inputBinding:
        position: 8
        prefix: --color_expression
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
  id: scombi-do-raster
  inputs:
    input_reference:
      doc: EO product 
      label: EO product 
      type: Directory
    red-band:
      doc: Common band name for red channel 
      label: Common band name for red channel 
      type: string
    green-band:
      doc: Common band name for green channel 
      label: Common band name for green channel 
      type: string?
    blue-band:
      doc: Common band name for blue channel 
      label: Common band name for blue channel 
      type: string?    
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
    color:
      doc: Color expression
      label: Area of interest
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
        inp1: input_reference
        inp2: input_reference
        inp3: input_reference
        inp4: red-band
        inp5: green-band
        inp6: blue-band
        inp7: aoi
        inp8: color
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
