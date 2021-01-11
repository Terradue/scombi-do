baseCommand: scombi-do
cwlVersion: v1.0
hints:
  DockerRequirement:
    dockerPull: terradue/scombi-do:0.1
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
  inp11:
    inputBinding:
      position: 11
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
      PATH: /opt/anaconda3/envs/env_scombi_do/bin/:/srv/conda/envs/env_scombi_do/bin/:/opt/anaconda/envs/env_scombi_do/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/envs/notebook/bin:/opt/anaconda/bin:/usr/share/java/maven/bin:/opt/anaconda/bin:/opt/anaconda/condabin:/opt/anaconda/bin:/usr/lib64/qt-3.3/bin:/usr/share/java/maven/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
      PREFIX: /opt/anaconda/envs/scombi_do
  ResourceRequirement: {}
#  stderr: std.err
stdout: std.out