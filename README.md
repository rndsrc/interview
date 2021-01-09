Interview is an interactive data viewing and inspecting framework for the Event Horizon Telescope.

Move your uvfits files to apps/uvfitsfiles/*

To add Baseline Stations(T1/T2) other than the ones in 2019 or 2020 EHT dataset,add them to apps/locations.txt
AND run apps/demo2.py to host app instead of apps/new.py

Supported color list : https://docs.bokeh.org/en/latest/docs/reference/colors.html



## Using Locally

### Setup

Clone this repository:
```
git clone https://rndsrc/interview.git
```
and [install Docker](https://docs.docker.com/install/) on your platform

### Building 

In the top level of this repository, execute the command
```
docker build --tag interview:bokehapp .
```

### Running

Execute the command to start the Docker container:
```
docker run --rm -p 5006:5006 -it interview:bokehapp
Go to dockerhub cli or use docker exec (docker exec -t -i interview:bokehapp /bin/bash)
cd interview
cd apps
bokeh serve --allow-websocket-origin="*" --num-procs=4 (max no of processes) new.py
```
Now navigate to ``http://localhost:5006`` to interact with the demo site. 

## Deploying to AWS
The bokeh server can be deployed using [Elastic Beanstalk with Docker Containers](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker.html). 

Random notes for future reference:

* Load balancer protocol needs to be set to TCP to allow websocket connections
* Similar rules needed to security group config
