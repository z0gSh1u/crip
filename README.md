# crip

A tool for Cone-Beam CT Data IO, Pre/Post-process and Physics.

## Quick Start

- Download the latest release from [Releases](https://github.com/z0gSh1u/crip/releases).

- Install the wheel by

  ```sh
  pip install /path/to/latest/release.whl
  ```

  Dependencies includes `numpy`, `opencv-python`, `pydicom` and `tifffile`.

- Import what you need to start coding.

## Modules

All functions are with clear documentation by comments. Just consider the function name and explore the source code, or refer to examples to start.

- `crip.io` for file input and output (RAW, DICOM and TIFF supported.)
- `crip.physics` for CT physics calculation.
- `crip.postprocess` for data post-processing.
- `crip.preprocess` for data pre-processing.
- `crip.shared` for common operations.

## Example

See [example](./example) here.

## Roadmap

crip is still under development. More features will be added in the future.

## Opensource License

MIT

