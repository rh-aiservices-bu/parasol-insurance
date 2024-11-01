import kfp
import kfp.dsl as dsl
from kfp.dsl import (
    component,
    Input,
    Output,
    Dataset,
    Metrics,
)
from kfp import kubernetes

from process_claims_pipeline import process_claims_pipeline

COMPILE=True

metadata = {
        "claim_ids": 0,
        "detection_endpoint": "https://some-endpoint",
    }

if COMPILE:
    kfp.compiler.Compiler().compile(process_claims_pipeline, 'process-claims-pipeline.yaml', pipeline_parameters = metadata)
else:
    namespace_file_path =\
        '/var/run/secrets/kubernetes.io/serviceaccount/namespace'
    with open(namespace_file_path, 'r') as namespace_file:
        namespace = namespace_file.read()

    kubeflow_endpoint =\
        f'https://ds-pipeline-dspa.{namespace}.svc:8443'

    sa_token_file_path = '/var/run/secrets/kubernetes.io/serviceaccount/token'
    with open(sa_token_file_path, 'r') as token_file:
        bearer_token = token_file.read()

    ssl_ca_cert =\
        '/var/run/secrets/kubernetes.io/serviceaccount/service-ca.crt'

    print(f'Connecting to Data Science Pipelines: {kubeflow_endpoint}')
    client = kfp.Client(
        host=kubeflow_endpoint,
        existing_token=bearer_token,
        ssl_ca_cert=ssl_ca_cert
    )

    print(f'Creating run with metadata: {metadata}')
    client.create_run_from_pipeline_func(
        process_claims_pipeline,
        arguments=metadata,
        experiment_name="process-claims",
        enable_caching=False
    )