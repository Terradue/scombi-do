baseCommand: docker
cwlVersion: v1.0
class: CommandLineTool
id: docker-builder
inputs:
  context:
    type: Directory
  dockerfile:
    type: File
arguments:
  - build
  - prefix: -t
    valueFrom: terradue/scombi-do:0.1
  - prefix: -f
    valueFrom: $(inputs.dockerfile)
  - valueFrom: $(inputs.context.path)
outputs:
  nothing:
    outputBinding:
      glob: .
    type: Directory

requirements:
  InlineJavascriptRequirement: {}