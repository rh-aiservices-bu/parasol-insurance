#!/bin/bash
user_count=$(oc get namespaces | grep showroom | wc -l)

MINIO_ROOT_USER=$(oc get secret minio-root-user -n ic-shared-minio -o template --template '{{.data.MINIO_ROOT_USER|base64decode}}')
MINIO_ROOT_PASSWORD=$(oc get secret minio-root-user -n ic-shared-minio -o template --template '{{.data.MINIO_ROOT_PASSWORD|base64decode}}')
MINIO_HOST=https://$(oc get route minio-s3 -n ic-shared-minio -o template --template '{{.spec.host}}')
DASHBOARD_ROUTE=https://$(oc get route rhods-dashboard -n redhat-ods-applications -o jsonpath='{.spec.host}')

# Define some variables
WORKBENCH_NAME="my-workbench"
WORKBENCH_IMAGE="ic-workbench:3.0.4"
PIPELINE_ENGINE="Tekton"
projects_without_running_pods=()
BRANCH_NAME="dev"

for i in $(seq 1 $user_count);
do

# Construct dynamic variables
USER_NAME="user$i"
USER_PROJECT="user$i"

if [ -z "$(oc get pods -n $USER_PROJECT -l app=$WORKBENCH_NAME -o custom-columns=STATUS:.status.phase --no-headers | grep Running)" ]; then
    echo "$USER_PROJECT workbench is not running."
    projects_without_running_pods+=("$USER_PROJECT")
fi

done

while true; do
  read -p "Do you want to recreate the above users? (y/n) " yn
    case $yn in
      [Yy]* ) break;;
      [Nn]* ) exit;;
      * ) echo "Please answer yes or no.";;
    esac
done


for USER_PROJECT in "${projects_without_running_pods[@]}"; 
do

# Assume username and user project is the same
USER_NAME=$USER_PROJECT

echo "Deleting user $USER_PROJECT..."
oc delete project $USER_PROJECT
echo "Waiting for project $USER_PROJECT to be deleted..."
while oc get project "$USER_PROJECT" &> /dev/null; do
  echo -n '.'
  sleep 5
done

echo "Generating and apply resources for $USER_NAME..."

# Create projects
cat << EOF | oc apply -f-
apiVersion: project.openshift.io/v1
kind: Project
metadata:
  annotations:
    openshift.io/description: ''
    openshift.io/display-name: $USER_PROJECT
  labels:
    kubernetes.io/metadata.name: $USER_PROJECT
    modelmesh-enabled: 'false'
    opendatahub.io/dashboard: 'true'
  name: $USER_PROJECT
spec:
  finalizers:
  - kubernetes
EOF

# Apply role bindings
cat << EOF | oc apply -f-
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: admin
  namespace: $USER_PROJECT
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: $USER_NAME
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: demo-setup
  namespace: $USER_PROJECT
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: demo-setup-edit
  namespace: $USER_PROJECT
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: edit
subjects:
- kind: ServiceAccount
  name: demo-setup
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: demo-setup-route-reader-binding-$USER_PROJECT
subjects:
- kind: ServiceAccount
  name: demo-setup
  namespace: $USER_PROJECT
roleRef:
  kind: ClusterRole
  name: route-reader
  apiGroup: rbac.authorization.k8s.io
---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: elyra-pipelines-$WORKBENCH_NAME
  namespace: $USER_PROJECT
  labels:
    opendatahub.io/dashboard: 'true'
subjects:
  - kind: ServiceAccount
    name: $WORKBENCH_NAME
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: ds-pipeline-user-access-pipelines-definition
EOF

# Create Data Science Connections
cat << EOF | oc apply -f-
apiVersion: batch/v1
kind: Job
metadata:
  name: create-ds-connections
  namespace: $USER_PROJECT
spec:
  selector: {}
  template:
    spec:
      containers:
      - args:
        - -ec
        - |-
          echo -n "Waiting for minio-root-user to exist"
          while [ -z "\$(oc get secret -n ic-shared-minio minio-root-user -oname 2>/dev/null)" ]; do
            echo -n '.'
            sleep 1
          done; echo

          echo "Minio user: $MINIO_ROOT_USER"
          echo "Minio pass: $MINIO_ROOT_PASSWORD"
          echo "Internal service url: http://minio.ic-shared-minio.svc.cluster.local:9000/"
          cat << EOF | oc apply -f-
          apiVersion: v1
          kind: Secret
          metadata:
            name: aws-connection-shared-minio---pipelines
            labels:
              opendatahub.io/dashboard: "true"
              opendatahub.io/managed: "true"
            annotations:
              opendatahub.io/connection-type: s3
              openshift.io/display-name: Shared Minio - pipelines
          type: Opaque
          stringData:
            AWS_ACCESS_KEY_ID: $MINIO_ROOT_USER
            AWS_SECRET_ACCESS_KEY: $MINIO_ROOT_PASSWORD
            AWS_DEFAULT_REGION: us
            AWS_S3_ENDPOINT: http://minio.ic-shared-minio.svc:9000
            AWS_S3_BUCKET: $USER_NAME
          EOF
        command:
        - /bin/bash
        image: quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:95b359257a7716b5f8d3a672081a84600218d8f58ca720f46229f7bb893af2ab
        imagePullPolicy: IfNotPresent
        name: create-ds-connections
      restartPolicy: Never
      serviceAccount: demo-setup
      serviceAccountName: demo-setup
EOF

# Set up the pipeline server
cat << EOF | oc apply -f-
apiVersion: datasciencepipelinesapplications.opendatahub.io/v1alpha1
kind: DataSciencePipelinesApplication
metadata:
  finalizers:
  - datasciencepipelinesapplications.opendatahub.io/finalizer
  name: pipelines-definition
  namespace: $USER_PROJECT
spec:
  apiServer:
    applyTektonCustomResource: true
    archiveLogs: false
    autoUpdatePipelineDefaultVersion: true
    collectMetrics: true
    dbConfigConMaxLifetimeSec: 120
    deploy: true
    enableOauth: true
    enableSamplePipeline: false
    injectDefaultScript: true
    stripEOF: true
    terminateStatus: Cancelled
    trackArtifacts: true
  database:
    mariaDB:
      deploy: true
      pipelineDBName: mlpipeline
      pvcSize: 10Gi
      username: mlpipeline
  objectStorage:
    externalStorage:
      bucket: $USER_NAME
      host: minio.ic-shared-minio.svc.cluster.local:9000
      port: ''
      s3CredentialsSecret:
        accessKey: AWS_ACCESS_KEY_ID
        secretKey: AWS_SECRET_ACCESS_KEY
        secretName: aws-connection-shared-minio---pipelines
      scheme: http
      secure: false
  persistenceAgent:
    deploy: true
    numWorkers: 2
  scheduledWorkflow:
    cronScheduleTimezone: UTC
    deploy: true
EOF

# Create the Elyra secret
cat << EOF | oc apply -f-
apiVersion: batch/v1
kind: Job
metadata:
  name: create-pipeline-secret
  namespace: $USER_PROJECT
spec:
  selector: {}
  template:
    spec:
      containers:
      - args:
        - -ec
        - |-
          echo -n 'Waiting for ds-pipeline-pipelines-definition route'
          while ! oc get route ds-pipeline-pipelines-definition 2>/dev/null; do
            echo -n .
            sleep 5
          done; echo

          PIPELINE_ROUTE=https://\$(oc get route ds-pipeline-pipelines-definition -o jsonpath='{.spec.host}')

          cat << EOF | oc apply -f-
          apiVersion: v1
          kind: Secret
          metadata:
            name: ds-pipeline-config
            namespace: $USER_PROJECT
          stringData:
            odh_dsp.json: '{"display_name": "Data Science Pipeline", "metadata": {"tags": [],
              "display_name": "Data Science Pipeline", "engine": "$PIPELINE_ENGINE", "auth_type": "KUBERNETES_SERVICE_ACCOUNT_TOKEN",
              "api_endpoint": "\$PIPELINE_ROUTE",
              "public_api_endpoint": "$DASHBOARD_ROUTE/pipelineRuns/$USER_PROJECT/pipelineRun/view/",
              "cos_auth_type": "KUBERNETES_SECRET", "cos_secret": "aws-connection-shared-minio---pipelines",
              "cos_endpoint": "$MINIO_HOST", "cos_bucket": "$USER_NAME",
              "cos_username": "$MINIO_ROOT_USER", "cos_password": "$MINIO_ROOT_PASSWORD",
              "runtime_type": "KUBEFLOW_PIPELINES"}, "schema_name": "kfp"}'
          type: Opaque
          EOF
        command:
        - /bin/bash
        image: quay.io/openshift-release-dev/ocp-v4.0-art-dev@sha256:95b359257a7716b5f8d3a672081a84600218d8f58ca720f46229f7bb893af2ab
        imagePullPolicy: IfNotPresent
        name: create-ds-connections
      restartPolicy: Never
      serviceAccount: demo-setup
      serviceAccountName: demo-setup
EOF

# Create the workbench PVC
cat << EOF | oc apply -f-
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  annotations:
    openshift.io/description: ''
    openshift.io/display-name: My Workbench
    volume.beta.kubernetes.io/storage-provisioner: openshift-storage.rbd.csi.ceph.com
    volume.kubernetes.io/storage-provisioner: openshift-storage.rbd.csi.ceph.com
  name: $WORKBENCH_NAME
  namespace: $USER_PROJECT
  finalizers:
    - kubernetes.io/pvc-protection
  labels:
    opendatahub.io/dashboard: 'true'
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: ocs-storagecluster-ceph-rbd
  volumeMode: Filesystem
EOF

# Create the workbench
cat << EOF | oc apply -f-
apiVersion: kubeflow.org/v1
kind: Notebook
metadata:
  annotations:
    notebooks.opendatahub.io/inject-oauth: 'true'
    opendatahub.io/image-display-name: CUSTOM - Parasol Insurance Claim Processing Lab Workbench
    notebooks.opendatahub.io/oauth-logout-url: >-
      $DASHBOARD_ROUTE/projects/$USER_PROJECT?notebookLogout=$WORKBENCH_NAME
    opendatahub.io/accelerator-name: ''
    openshift.io/description: ''
    openshift.io/display-name: My Workbench
    notebooks.opendatahub.io/last-image-selection: '$WORKBENCH_IMAGE'
    notebooks.opendatahub.io/last-size-selection: Standard
    opendatahub.io/username: $USER_NAME
  name: $WORKBENCH_NAME
  namespace: $USER_PROJECT
  labels:
    app: $WORKBENCH_NAME
    opendatahub.io/dashboard: 'true'
    opendatahub.io/odh-managed: 'true'
    opendatahub.io/user: $USER_NAME
spec:
  template:
    spec:
      affinity: {}
      containers:
        - resources:
            limits:
              cpu: '2'
              memory: 8Gi
            requests:
              cpu: '1'
              memory: 6Gi
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /notebook/$USER_PROJECT/$WORKBENCH_NAME/api
              port: notebook-port
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
          name: $WORKBENCH_NAME
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /notebook/$USER_PROJECT/$WORKBENCH_NAME/api
              port: notebook-port
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
          env:
            - name: NOTEBOOK_ARGS
              value: |-
                --ServerApp.port=8888
                                  --ServerApp.token=''
                                  --ServerApp.password=''
                                  --ServerApp.base_url=/notebook/$USER_PROJECT/$WORKBENCH_NAME
                                  --ServerApp.quit_button=False
                                  --ServerApp.tornado_settings={"user":"$USER_NAME","hub_host":"$DASHBOARD_ROUTE","hub_prefix":"/projects/$USER_PROJECT"}
            - name: JUPYTER_IMAGE
              value: >-
                image-registry.openshift-image-registry.svc:5000/redhat-ods-applications/$WORKBENCH_IMAGE
          ports:
            - containerPort: 8888
              name: notebook-port
              protocol: TCP
          imagePullPolicy: Always
          volumeMounts:
            - mountPath: /opt/app-root/src
              name: $WORKBENCH_NAME
            - mountPath: /opt/app-root/runtimes
              name: elyra-dsp-details
            - mountPath: /dev/shm
              name: shm
          image: >-
            image-registry.openshift-image-registry.svc:5000/redhat-ods-applications/$WORKBENCH_IMAGE
          workingDir: /opt/app-root/src
        - resources:
            limits:
              cpu: 100m
              memory: 64Mi
            requests:
              cpu: 100m
              memory: 64Mi
          readinessProbe:
            failureThreshold: 3
            httpGet:
              path: /oauth/healthz
              port: oauth-proxy
              scheme: HTTPS
            initialDelaySeconds: 5
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
          name: oauth-proxy
          livenessProbe:
            failureThreshold: 3
            httpGet:
              path: /oauth/healthz
              port: oauth-proxy
              scheme: HTTPS
            initialDelaySeconds: 30
            periodSeconds: 5
            successThreshold: 1
            timeoutSeconds: 1
          env:
            - name: NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - containerPort: 8443
              name: oauth-proxy
              protocol: TCP
          imagePullPolicy: Always
          volumeMounts:
            - mountPath: /etc/oauth/config
              name: oauth-config
            - mountPath: /etc/tls/private
              name: tls-certificates
          image: >-
            registry.redhat.io/openshift4/ose-oauth-proxy@sha256:4bef31eb993feb6f1096b51b4876c65a6fb1f4401fee97fa4f4542b6b7c9bc46
          args:
            - '--provider=openshift'
            - '--https-address=:8443'
            - '--http-address='
            - '--openshift-service-account=$WORKBENCH_NAME'
            - '--cookie-secret-file=/etc/oauth/config/cookie_secret'
            - '--cookie-expire=24h0m0s'
            - '--tls-cert=/etc/tls/private/tls.crt'
            - '--tls-key=/etc/tls/private/tls.key'
            - '--upstream=http://localhost:8888'
            - '--upstream-ca=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
            - '--email-domain=*'
            - '--skip-provider-button'
            - >-
              --openshift-sar={"verb":"get","resource":"notebooks","resourceAPIGroup":"kubeflow.org","resourceName":"$WORKBENCH_IMAGE","namespace":"$USER_PROJECT"}
            - >-
              --logout-url=$DASHBOARD_ROUTE/projects/$USER_PROJECT?notebookLogout=$WORKBENCH_IMAGE
      enableServiceLinks: false
      serviceAccountName: $WORKBENCH_NAME
      tolerations:
        - effect: NoSchedule
          key: notebooksonly
          operator: Exists
      volumes:
        - name: $WORKBENCH_NAME
          persistentVolumeClaim:
            claimName: $WORKBENCH_NAME
        - name: elyra-dsp-details
          secret:
            secretName: ds-pipeline-config
        - emptyDir:
            medium: Memory
          name: shm
        - name: oauth-config
          secret:
            defaultMode: 420
            secretName: $WORKBENCH_NAME-oauth-config
        - name: tls-certificates
          secret:
            defaultMode: 420
            secretName: $WORKBENCH_NAME-tls
  readyReplicas: 1
EOF

# Git clone job
cat << EOF | oc apply -f-
apiVersion: batch/v1
kind: Job
metadata:
  name: clone-repo
  namespace: $USER_PROJECT
spec:
  backoffLimit: 4
  template:
    spec:
      serviceAccount: demo-setup
      serviceAccountName: demo-setup
      initContainers:
      - name: wait-for-workbench
        image: image-registry.openshift-image-registry.svc:5000/openshift/tools:latest
        imagePullPolicy: IfNotPresent
        command: ["/bin/bash"]
        args:
        - -ec
        - |-
          echo -n "Waiting for workbench pod in $USER_PROJECT namespace"
          while [ -z "\$(oc get pods -n $USER_PROJECT -l app=$WORKBENCH_NAME -o custom-columns=STATUS:.status.phase --no-headers | grep Running 2>/dev/null)" ]; do
              echo -n '.'
              sleep 1
          done
          echo "Workbench pod is running in $USER_PROJECT namespace"
      containers:
      - name: git-clone
        image: image-registry.openshift-image-registry.svc:5000/openshift/tools:latest
        imagePullPolicy: IfNotPresent
        command: ["/bin/bash"]
        args:
        - -ec
        - |-
          pod_name=\$(oc get pods --selector=app=$WORKBENCH_NAME -o jsonpath='{.items[0].metadata.name}') && oc exec \$pod_name -- git clone https://github.com/TroyNelson11/parasol-insurance && cd parasol-insurance && git checkout $BRANCH_NAME
      restartPolicy: Never
EOF

done