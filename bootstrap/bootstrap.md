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