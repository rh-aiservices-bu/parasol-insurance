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

@dsl.container_component
def initialize():
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c', 
            '''cd /shared-data
            rm -r * 2>/dev/null
            git clone https://github.com/rh-aiservices-bu/parasol-insurance
            cd parasol-insurance
            git checkout main-rhoai-2.13
            ls
            ''',
        ],
        args=[]
    )

@dsl.container_component
def get_claims(claim_ids: int):
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''claim_id="$0"
            export claim_id=$claim_id
            export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python get_claims.py
            ''',
        ],
        args=[claim_ids]
    )

@dsl.container_component
def get_accident_time():
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python get_accident_time.py
            ''',
        ],
        args=[]
    )

@dsl.container_component
def get_location():
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python get_location.py
            ''',
        ],
        args=[]
    )

@dsl.container_component
def get_sentiment():
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python get_sentiment.py
            ''',
        ],
        args=[]
    )

@dsl.container_component
def detect_objects(detection_endpoint: str):
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''detection_endpoint="$0"
            export detection_endpoint=$detection_endpoint
            export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python detect_objects.py
            ''',
        ],
        args=[detection_endpoint]
    )

@dsl.container_component
def summarize_text():
    return dsl.ContainerSpec(
        image='quay.io/rh-aiservices-bu/rhoai-lab-insurance-claim-processing-pipeline:1.2', 
        command=[
            'sh',
            '-c',
            '''export POSTGRES_HOST=claimdb.$NAMESPACE.svc.cluster.local
            export IMAGES_BUCKET=$NAMESPACE
            cd /shared-data
            cd parasol-insurance/lab-materials/05/05-05
            python summarize_text.py
            ''',
        ],
        args=[]
    )