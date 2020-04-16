ocs-metadata
============
[![Docker Repository on Quay](https://quay.io/repository/zmc/ocs-metadata/status "Docker Repository on Quay")](https://quay.io/repository/zmc/ocs-metadata)

A cloud-native application to store metadata for [OpenShift Container Storage](https://www.openshift.com/products/container-storage/) product versions, and the component images that they are built from.

It is built with [python-eve](https://python-eve.org/), using [MongoDB](https://www.mongodb.com/) for backend storage. Build metadata may be submitted with an HTTP POST request to `/builds` that looks like:

    {
      "product": "OCS",
      "url": "https://jenkins.example.com/job/ocs-registry-container/42",
      "version": 4.0.0-42",
      "contents": [
        {
          "name": "ocs-operator",
          "tag": "4.0-1",
          "image": "quay.io/example_org/ocs-operator@sha256:xxx",
          "nvr": "ocs-operator-container-4.0-1.xxx"
        },
        ...
      ]
    }


To query, simply GET `/builds/` or `/builds/<version>` (using the example above, `/builds/4.0.0-42`).


Populating builds from Jenkins
------------------------------
A basic script to pull build data from our [Jenkins](https://jenkins.io/) pipeline is provided; it
will likely require modification to work with any others:

    # Attempt to pull metadata from all builds of the ocs-registry-container job
    ./scrape.py -u https://jenkins.example.com/
    # Use a different job name
    ./scrape.py -u https://jenkins.example.com/ -j my-ocs-registry-job
    # Pull from a single build
    ./scrape.py -u https://jenkins.example.com -b 42
    # Pull from a Jenkins with a self-signed certificate
    PYTHONHTTPSVERIFY=0 ./scrape.py -u https://jenkins.example.com/

While submitting single builds via `curl` is trivial, submitting many builds is easier with this basic companion script:

    # Submit builds from a file
    ./submit.py -u https://ocs-metadata.example.com ./builds.json
    # Submit builds from stdin
    ./submit.py -u https://ocs-metadata.example.com -


Deploying
---------
First, write a `.env` file in the root of this repo. It should look like this:

    MONGO_INITDB_ROOT_USERNAME=root
    MONGO_INITDB_ROOT_PASSWORD=redacted
    ME_CONFIG_MONGODB_ADMINUSERNAME=root
    ME_CONFIG_MONGODB_ADMINPASSWORD=redacted
    MONGO_USERNAME=root
    MONGO_PASSWORD=redacted

To deploy to OpenShift:

    kompose up --provider openshift --build none

To deploy locally via docker:

    docker-compose up


Building
--------
For mongo and mongo-express, we use stock images. For the API, we build the ocs-metadata image like so:

    docker-compose build --no-cache
    docker push quay.io/zmc/ocs-metadata
