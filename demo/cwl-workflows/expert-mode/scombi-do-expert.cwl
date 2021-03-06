$graph:
- baseCommand: scombi-do
  arguments: [--resolution, 'highest'] 
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
      type:
        type: array
        items: string
        inputBinding:
          prefix: --s_expression
      inputBinding:
        position: 7
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
        PATH: /srv/conda/envs/notebook/bin/:/Applications/miniforge3/envs/env_scombi_do/bin/:/opt/anaconda3/envs/env_scombi_do/bin/:/srv/conda/envs/env_scombi_do/bin/:/opt/anaconda/envs/env_scombi_do/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/scombi_do
    ResourceRequirement: {}
#  stderr: std.err
  stdout: std.out
- class: Workflow
  doc: This step combines three bands as an RGB composite
  id: expert
  inputs:
    input_reference_1:
      doc: EO product 
      label: EO product 
      type: Directory
    input_reference_2:
      doc: EO product 
      label: EO product 
      type: Directory?
    input_reference_3:
      doc: EO product 
      label: EO product 
      type: Directory?
    band_1:
      doc: A common band name 
      label: A common band name 
      type: string
    band_2:
      doc: A common band name 
      label: A common band name 
      type: string?
    band_3:
      doc: A common band name 
      label: A common band name 
      type: string? 
    s_expression:
      doc: one or more s expressions
      label: one or more s expressions
      type: string[]  
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
    color:
      doc: Color expression
      label: Area of interest
      type: string?
    lut:
      doc: Look-up table
      label: Look-up table
      type: string?
  label: Multitemporal band combination
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
        inp3: input_reference_3
        inp4: band_1
        inp5: band_2
        inp6: band_3
        inp7: s_expression
        inp8: aoi
        inp9: color
        inp10: lut
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
