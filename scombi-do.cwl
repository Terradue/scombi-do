$graph:
- baseCommand: scombi-do
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
        prefix: --resolution
      type: string
    inp8:
      inputBinding:
        position: 8
        prefix: --aoi
      type: string?
    inp9:
      inputBinding:
        position: 9
        prefix: --color_expression
      type: string? 
    inp10:
      inputBinding:
        position: 10
        prefix: --profile
      type: string?
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /srv/conda/envs/env_scombi_do/bin/:/opt/anaconda/envs/env_scombi_do/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/scombi_do
    ResourceRequirement: {}
#  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: This step combines three bands as an RGB composite
  id: scombi-do
  inputs:
    red-channel-input:
      doc: EO product for red channel
      label: EO product for red channel
      type: Directory
    green-channel-input:
      doc: EO product for green channel
      label: EO product for green channel
      type: Directory?
    blue-channel-input:
      doc: EO product for blue channel
      label: EO product for blue channel
      type: Directory?
    red-band:
      doc: Common band name for red channel input
      label: Common band name for red channel input
      type: string
    green-band:
      doc: Common band name for green channel input
      label: Common band name for green channel input
      type: string?
    blue-band:
      doc: Common band name for blue channel input
      label: Common band name for blue channel input
      type: string?    
    resolution:
      doc: Resolution approach
      label: Resolution approach
      type: string 
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
    color:
      doc: Color expression
      label: Area of interest
      type: string?
    profile:
      doc: profile expression
      label: profile
      type: string?
  label: Band combination
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type:
      Directory
  steps:
    node_1:
      in:
        inp1: red-channel-input
        inp2: green-channel-input
        inp3: blue-channel-input
        inp4: red-band
        inp5: green-band
        inp6: blue-band
        inp7: resolution
        inp8: aoi
        inp9: color
        inp10: profile
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
