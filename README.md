# OpenShift AI Unleashed: Transforming Claims Processing for Maximum Efficiency!

## Introduction

This repository contains the code, instructions, resources and materials associated with the Lab called **OpenShift AI Unleashed: Transforming Claims Processing for Maximum Efficiency!**.

To consult the static version of the instructions, please use [this URL](https://rh-aiservices-bu.github.io/parasol-insurance/)

If you want to participate in the creation and update of this content, please consult the sections below.

<details>
  <summary>Display Development-centric information</summary>

## General Development Information

### Working with this repo

- `main` branch is the one used for production. That's where the Prod and Test catalog items from [demo.redhat.com](https://demo.redhat.com) point to (instructions, materials used,...).
- `dev` branch is for development. That's where the Dev catalog item points to.
- Branches are made from `dev` (hot fixes could be made from `main` if really needed).
- When ready, PRs should be made to `dev`. Once all features, bug fixes,... are checked in and tested for a new release, another PR will be made from `dev` to `main`.
- Branches must be prefixed with `/feature` (example `feature/new-pipeline-instructions`), `bugfix`, or other meaningful info.
- Add your name/handle in the branch name if needed to avoid confusion.
- If your development relates to an Issue or a Feature Request, add its reference in the branch name.
- Try to stash your changes before submitting a PR.

## How to update the **Instructions**

Useful link: [https://redhat-scholars.github.io/build-course/rhs-build-course/develop.html](https://redhat-scholars.github.io/build-course/rhs-build-course/develop.html)

### Requirements

- Podman or Docker

### Development

- Add/Modify/Delete content in [content/modules/ROOT](content/modules/ROOT).
- Navigation is handled in `nav.adoc`.
- Content pages are in the `pages` folder.
- To build the site, from the root of the repo, run `./content/utilities/lab-build`.
- To serve the site for previewing, from the root of the repo, run `./content/utilities/lab-serve`.
- The site will be visible at [http://localhost:8443/](http://localhost:8443/)
- When finished, you can stop serving the site by running from the root of the repo `./content/utilities/lab-stop`.

## How to update the **Application**

### Requirements

- Python 3.11
- Nodejs > 18
- An existing instance of Hugging Face TGI with a loaded model available at `INFERENCE_SERVER_URL`. This application is based on Mistral-TB Prompt format. You will need to modify this format if you are using a different model.

### Installation

Run `npm install` from the main folder.

If you want to install packages manually:

- In the `frontend` folder, install the node modules with `npm install`.
- In the `backend` folder, create a venv and install packages with the provided Pipfile/Pipfile.lock files.
- In the `backend` folder, create the file `.env` base on the example `.env.example` and enter the configuration for the Inference server.

### Development

From the main folder, launch `npm run dev` or `./start-dev.sh`. This will launch both backend and frontend.

- Frontend is accessible at `http://localhost:9000`
- Backend is accessible at `http://localhost:5000`, with Swagger API doc at `http://localhost:5000/docs`

```bash
#!/bin/bash

# Script to restart all showroom pods - You must be logged in as a cluster admin to run this script

# Get all namespaces
namespaces=$(oc get namespaces -o jsonpath='{.items[*].metadata.name}' \
    | tr ' ' '\n' \
    | grep '^showroom')

# Stop all the pods
for namespace in $namespaces; do
    # Check if the deployment "showroom" exists in the namespace
    if oc -n $namespace get deployment showroom &> /dev/null; then
        # If it exists, restart the rollout
        # oc -n $namespace rollout restart deployment/showroom
        oc -n $namespace scale deploy showroom --replicas=0
    fi
done


# wait for them all to fully stop
# start all the pods
for namespace in $namespaces; do
    # Check if the deployment "showroom" exists in the namespace
    if oc -n $namespace get deployment showroom &> /dev/null; then
        # If it exists, restart the rollout
        # oc -n $namespace rollout restart deployment/showroom
        oc -n $namespace scale deploy showroom --replicas=1
    fi
done


```

## How to graduate code from dev to main

- From `dev`, create a new branch, like `feature/prepare-for-main-merge`.
- Modify the following files to make their relevant content point to `main`:
  - `bootstrap/applicationset/applicationset-bootstrap.yaml`
  - `content/antora.yml`
  - `content/modules/ROOT/pages/05-03-web-app-deploy-application.adoc`
- Make a pull request from this branch to `main`, review and merge

</details>

<details>
  <summary>Links for Summit event environment assignment</summary>

- URL for all labs: [https://one.demo.redhat.com/](https://one.demo.redhat.com/)
- Search for `parasol`

</details>
