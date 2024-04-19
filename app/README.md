# Application image

## Building

The npm build happens during the image build. To do it successfully, you may have to augment the limits on open files in your system. Ex:

`podman build --no-cache --ulimit nofile=10000:10000 -t rhoai-lab-insurance-claim-app:2.1.0 .`
