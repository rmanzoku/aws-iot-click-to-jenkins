# aws-iot-click-to-jenkins
AWS Lambda script.

[AWS IoT Enterprise Button](https://aws.amazon.com/iot-1-click/devices/) executes Jenkins build job.

## Support
- Build with parameter
- CSRF crumb request

## How to use
- Control click type by AWS IoT 1-click `Placements attributes` prefix.
  - `SINGLE_` for single click
  - `DOUBLE_` for double click
  - `LONG_` for single click
- Set IoT `Attribute` with `SINGLE_JOB`, `DOUBLE_JOB` or `LONG_JOB`.
- Build parameter binded by attributes like `SINGLE_VERSION` to `VERSION`.
