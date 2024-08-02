# Bootstrap info

## how to book the environment.


## how to configure the environment to use another branch

1. change all the argo apps:

    ```bash
    BR="rhoai-2-10"
    oc -n openshift-gitops get applicationset

    echo "   {argocd} UI : https://$(oc -n openshift-gitops \
         get route openshift-gitops-server \
         -ojsonpath='{.status.ingress[0].host}')/ "

    oc -n openshift-gitops get applicationset -o yaml > /tmp/parasol_apps.yaml
    sed -i.back 's/main/rhoai\-2\-10/g' /tmp/parasol_apps.yaml
    oc apply -f /tmp/parasol_apps.yaml


    ```

2. restart/update all the showroom pods

    ```bash
    #!/bin/bash

    for ns in $(oc get namespaces -o jsonpath="{.items[*].metadata.name}" \
        | tr ' ' '\n' \
        | grep '^showroom') ; do
        echo $ns
        oc -n $ns scale deploy showroom --replicas=0
        oc -n $ns patch deployment showroom  \
            --type='json' \
            -p='[{"op": "replace", "path": "/spec/template/spec/containers/1/env/1/value", "value": "rhoai-2-10"}]'
        oc -n $ns scale deploy showroom --replicas=1
    done

    ```



## older stuff

manually

```bash
GITEA_INT_URL="http://gitea.gitea.svc:3000/"
GITEA_REPO="opentlc-mgr/parasol-insurance-mirror/"
GITEA_BRANCH="dev/"
GITEA_APP_PATH="bootstrap/applications/ic-shared-minio-app.yaml"

CMD=" oc apply -f ${GITEA_INT_URL}${GITEA_REPO}raw/branch/${GITEA_BRANCH}${GITEA_APP_PATH}"

echo ${CMD}

oc apply -f ./bootstrap/applicationset/applicationset-bootstrap.yaml

```

<!--
# https://gitea.apps.cluster-rvl84.sandbox483.opentlc.com/opentlc-mgr/parasol-insurance-mirror/raw/branch/feature/minio-in-gitops/bootstrap/applications/ic-shared-minio-app.yaml
#echo "http://gitea.gitea.svc:3000/opentlc-mgr/parasol-insurance-mirror/raw/branch/feature/minio-in-gitops/bootstrap/applications/ic-shared-minio-app.yaml"
-->