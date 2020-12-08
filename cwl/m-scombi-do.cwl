$graph:
- class: Workflow
  doc: Main stage manager
  id: stage-manager
  inputs:
    aoi:
      doc: Area of interest in WKT
      id: aoi
      label: Area of interest
      type: string?
    blue-band:
      doc: Common band name for blue channel input
      id: blue-band
      label: Common band name for blue channel input
      type: string?
    blue-channel-input:
      doc: EO product for blue channel
      id: blue-channel-input
      label: EO product for blue channel
      type: string
    color:
      doc: Color expression
      id: color
      label: Area of interest
      type: string?
    green-band:
      doc: Common band name for green channel input
      id: green-band
      label: Common band name for green channel input
      type: string?
    green-channel-input:
      doc: EO product for green channel
      id: green-channel-input
      label: EO product for green channel
      type: string
    job:
      doc: ''
      id: job
      label: ''
      type: string
    lut:
      doc: lut
      id: lut
      label: lut
      type: string?
    outputfile:
      doc: ''
      id: outputfile
      label: ''
      type: string
    profile:
      doc: profile expression
      id: profile
      label: profile
      type: string?
    red-band:
      doc: Common band name for red channel input
      id: red-band
      label: Common band name for red channel input
      type: string
    red-channel-input:
      doc: EO product for red channel
      id: red-channel-input
      label: EO product for red channel
      type: string
    resolution:
      doc: Resolution approach
      id: resolution
      label: Resolution approach
      type: string
    store_apikey:
      doc: ''
      id: store_apikey
      label: ''
      type: string
    store_host:
      doc: ''
      id: store_host
      label: ''
      type: string
    store_username:
      doc: ''
      id: store_username
      label: ''
      type: string
  label: theStage
  outputs:
    wf_outputs:
      outputSource:
      - node_stage_out/wf_outputs_out
      type: Directory
  requirements:
    ScatterFeatureRequirement: {}
    SubworkflowFeatureRequirement: {}
  steps:
    node_stage_in:
      in:
        red-channel-input: red-channel-input
      out:
      - red-channel-input_out
      run:
        arguments:
        - position: 1
          prefix: -t
          valueFrom: ./
        baseCommand: stage-in
        class: CommandLineTool
        hints:
          DockerRequirement:
            dockerPull: eoepca/stage-in:0.2
        id: stagein
        inputs:
          red-channel-input:
            inputBinding:
              position: 2
            type: string
        outputs:
          red-channel-input_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              PATH: /opt/anaconda/envs/env_stagein/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          ResourceRequirement: {}
    node_stage_in_1:
      in:
        green-channel-input: green-channel-input
      out:
      - green-channel-input_out
      run:
        arguments:
        - position: 1
          prefix: -t
          valueFrom: ./
        baseCommand: stage-in
        class: CommandLineTool
        hints:
          DockerRequirement:
            dockerPull: eoepca/stage-in:0.2
        id: stagein
        inputs:
          green-channel-input:
            inputBinding:
              position: 2
            type: string
        outputs:
          green-channel-input_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              PATH: /opt/anaconda/envs/env_stagein/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          ResourceRequirement: {}
    node_stage_in_1_2:
      in:
        blue-channel-input: blue-channel-input
      out:
      - blue-channel-input_out
      run:
        arguments:
        - position: 1
          prefix: -t
          valueFrom: ./
        baseCommand: stage-in
        class: CommandLineTool
        hints:
          DockerRequirement:
            dockerPull: eoepca/stage-in:0.2
        id: stagein
        inputs:
          blue-channel-input:
            inputBinding:
              position: 2
            type: string
        outputs:
          blue-channel-input_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              PATH: /opt/anaconda/envs/env_stagein/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          ResourceRequirement: {}
    node_stage_out:
      in:
        job: job
        outputfile: outputfile
        store_apikey: store_apikey
        store_host: store_host
        store_username: store_username
        wf_outputs: on_stage/wf_outputs
      out:
      - wf_outputs_out
      run:
        baseCommand: stage-out
        class: CommandLineTool
        hints:
          DockerRequirement:
            dockerPull: eoepca/stage-out:0.2
        inputs:
          job:
            inputBinding:
              position: 1
              prefix: --job
            type: string
          outputfile:
            inputBinding:
              position: 5
              prefix: --outputfile
            type: string
          store_apikey:
            inputBinding:
              position: 4
              prefix: --store-apikey
            type: string
          store_host:
            inputBinding:
              position: 2
              prefix: --store-host
            type: string
          store_username:
            inputBinding:
              position: 3
              prefix: --store-username
            type: string
          wf_outputs:
            inputBinding:
              position: 6
            type: Directory
        outputs:
          wf_outputs_out:
            outputBinding:
              glob: .
            type: Directory
        requirements:
          EnvVarRequirement:
            envDef:
              PATH: /opt/anaconda/envs/env_stageout/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
          ResourceRequirement: {}
    on_stage:
      in:
        aoi: aoi
        blue-band: blue-band
        blue-channel-input: node_stage_in_1_2/blue-channel-input_out
        color: color
        green-band: green-band
        green-channel-input: node_stage_in_1/green-channel-input_out
        lut: lut
        profile: profile
        red-band: red-band
        red-channel-input: node_stage_in/red-channel-input_out
        resolution: resolution
      out:
      - wf_outputs
      run: '#scombi-do'
- baseCommand: scombi-do
  class: CommandLineTool
  hints:
    DockerRequirement:
      dockerPull: scombi:latest
  id: clt
  inputs:
    inp1:
      inputBinding:
        position: 1
        prefix: --red-channel-input
      type: Directory
    inp10:
      inputBinding:
        position: 10
        prefix: --profile
      type: string?
    inp11:
      inputBinding:
        position: 11
        prefix: --lut
      type: string?
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
  outputs:
    results:
      outputBinding:
        glob: .
      type: Directory
  requirements:
    EnvVarRequirement:
      envDef:
        PATH: /opt/anaconda3/envs/env_scombi_do/bin/:/srv/conda/envs/env_scombi_do/bin/:/opt/anaconda/envs/env_scombi_do/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
        PREFIX: /opt/anaconda/envs/scombi_do
    ResourceRequirement: {}
  stdout: std.out
- class: Workflow
  doc: This step combines three bands as an RGB composite
  id: scombi-do
  inputs:
    aoi:
      doc: Area of interest in WKT
      label: Area of interest
      type: string?
    blue-band:
      doc: Common band name for blue channel input
      label: Common band name for blue channel input
      type: string?
    blue-channel-input:
      doc: EO product for blue channel
      label: EO product for blue channel
      type: Directory?
    color:
      doc: Color expression
      label: Area of interest
      type: string?
    green-band:
      doc: Common band name for green channel input
      label: Common band name for green channel input
      type: string?
    green-channel-input:
      doc: EO product for green channel
      label: EO product for green channel
      type: Directory?
    lut:
      doc: lut
      label: lut
      type: string?
    profile:
      doc: profile expression
      label: profile
      type: string?
    red-band:
      doc: Common band name for red channel input
      label: Common band name for red channel input
      type: string
    red-channel-input:
      doc: EO product for red channel
      label: EO product for red channel
      type: Directory
    resolution:
      doc: Resolution approach
      label: Resolution approach
      type: string
  label: Band combination
  outputs:
  - id: wf_outputs
    outputSource:
    - node_1/results
    type: Directory
  steps:
    node_1:
      in:
        inp1: red-channel-input
        inp10: profile
        inp11: lut
        inp2: green-channel-input
        inp3: blue-channel-input
        inp4: red-band
        inp5: green-band
        inp6: blue-band
        inp7: resolution
        inp8: aoi
        inp9: color
      out:
      - results
      run: '#clt'
cwlVersion: v1.0
