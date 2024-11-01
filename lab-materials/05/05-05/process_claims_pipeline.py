# kfp imports
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

# Importing components
from pipeline_components import initialize, get_claims, get_accident_time, get_location, get_sentiment, detect_objects, summarize_text


@dsl.pipeline(
  name='process-claims-pipeline',
  description='Processes claims.'
)
def process_claims_pipeline(claim_ids: int, detection_endpoint: str):
    # Initialize by downloading the repo
    initialize_task = initialize()
    kubernetes.mount_pvc(
        task=initialize_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )

    # Get the unprocessed claims if none has been entered
    get_claims_task = get_claims(claim_ids=claim_ids)
    kubernetes.mount_pvc(
        task=get_claims_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    get_claims_task.after(initialize_task)
    kubernetes.use_field_path_as_env(
        get_claims_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )

    # Get accident time
    get_accident_time_task = get_accident_time()
    kubernetes.mount_pvc(
        task=get_accident_time_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    get_accident_time_task.after(get_claims_task)
    kubernetes.use_field_path_as_env(
        get_accident_time_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )

    # Get location
    get_location_task = get_location()
    kubernetes.mount_pvc(
        task=get_location_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    get_location_task.after(get_claims_task)
    kubernetes.use_field_path_as_env(
        get_location_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )

    # Get sentiment
    get_sentiment_task = get_sentiment()
    kubernetes.mount_pvc(
        task=get_sentiment_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    get_sentiment_task.after(get_claims_task)
    kubernetes.use_field_path_as_env(
        get_sentiment_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )

    # Detect objects
    detect_objects_task = detect_objects(detection_endpoint=detection_endpoint)
    kubernetes.mount_pvc(
        task=detect_objects_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    detect_objects_task.after(get_claims_task)
    kubernetes.use_field_path_as_env(
        detect_objects_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )

    # Summarize text
    summarize_text_task = summarize_text()
    kubernetes.mount_pvc(
        task=summarize_text_task,
        pvc_name="processing-pipeline-storage",
        mount_path="/shared-data",
    )
    summarize_text_task.after(get_claims_task)
    kubernetes.use_field_path_as_env(
        summarize_text_task,
        env_name='NAMESPACE',
        field_path='metadata.namespace'
    )