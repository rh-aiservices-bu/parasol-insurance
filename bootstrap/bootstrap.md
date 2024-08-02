# Bootstrap info

## how to book the environment.

This [link](https://demo.redhat.com/catalog?item=babylon-catalog-prod/sandboxes-gpte.openshift-ai-unleashed.prod&utm_source=webapp&utm_medium=share-link) in the demo system.



## how to configure the environment to use another branch

1. change all the argo apps:

    ```bash
    BR="rhoai-2-10"
    BR="rhoai-2-10-test-dspa"
    oc -n openshift-gitops get applicationset

    echo "   {argocd} UI : https://$(oc -n openshift-gitops \
         get route openshift-gitops-server \
         -ojsonpath='{.status.ingress[0].host}')/ "

    echo "   {argocd} admin pass : $(oc get secret openshift-gitops-cluster \
        -n openshift-gitops \
        -o jsonpath='{.data.admin\.password}' \
        | base64 -d) "

    echo "updating apps"

    ## delete the apps
    oc -n openshift-gitops delete applicationset bootstrap

    ## re-apply from branch
    oc apply -f https://raw.githubusercontent.com/rh-aiservices-bu/parasol-insurance/$BR/bootstrap/applicationset/applicationset-bootstrap.yaml

    ## change branch in all apps
    oc -n openshift-gitops get applicationset bootstrap -o json | \
        jq ".spec.generators[0].list.elements |= map(.targetRevision = \"$BR\")" | \
        oc -n openshift-gitops apply -f -

    # conflicts in operator groups
    oc -n redhat-ods-operator delete OperatorGroup --all


    ## delete and re-create all the user projects
    for ns in $(oc get namespaces -o jsonpath="{.items[*].metadata.name}" \
        | tr ' ' '\n' \
        | grep '^user') ; do
        echo $ns
        oc delete ns $ns
    done

    ## trigger a sync of the project creation

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
            -p="[{'op': 'replace', 'path': '/spec/template/spec/containers/1/env/1/value', 'value': \"$BR\"}]"
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