#!/usr/bin/env cwltool
class: Workflow
doc: This step combines three bands as an RGB composite
id: main
inputs:
  context:
    type: Directory
  dockerfile:
    type: File
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
  lut:
    doc: lut
    label: lut
    type: string?
label: Band combination
outputs:
  - id: wf_outputs
    outputSource:
      - step_1/results
    type:
      Directory
requirements:
  - class: SubworkflowFeatureRequirement
steps:
  step_0:
    in:
      context: context
      dockerfile: dockerfile
    out:
      - nothing
    run: '_docker-builder.cwl'
  step_1:
    in:
      inp0: step_0/nothing
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
      inp11: lut
    out:
      - results
    run: '_scombi-do.cwl'
cwlVersion: v1.0