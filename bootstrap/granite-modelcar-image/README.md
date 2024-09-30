# Granite ModelCar Image

Based on the [KServe Modelcars approach](https://kserve.github.io/website/latest/modelserving/storage/oci/), the Containerfile is used to build a custom Container Image that includes the [Granite 7B Instruct](https://huggingface.co/ibm-granite/granite-7b-instruct) model.

## Building the image

To build the image, use the following command:

`podman build -t granite-7b-instruct-modelcar:x.y .`

## Using the Granite Modelcar Container Image in KServe

Modelcars is not enabled by default in KServe. To enable this model serving method, it needs to be activated in the [KServe configuration](https://kserve.github.io/website/latest/modelserving/storage/oci/#enabling-modelcars).

In this workshop, the modelCar is enabled in a [Job](../ic-shared-llm/job-enable-modelcar.yaml) that is deployed during the bootstrap.