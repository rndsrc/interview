FROM continuumio/miniconda
ENV BK_VERSION=2.1.0
ENV PY_VERSION=3.7
ENV NUM_PROCS=4
ENV BOKEH_RESOURCES=cdn

RUN apt-get install git bash
RUN git clone --branch eq_editor_alpha https://github.com/phanicode/interview.git
COPY requirements.txt ./

RUN conda config --append channels bokeh
RUN conda install --yes python=${PY_VERSION} jinja2 bokeh=${BK_VERSION} numpy ephem seaborn matplotlib  scipy sympy "nodejs>=8.8" pandas flask
RUN conda install --yes pyyaml=5.3.1
RUN conda clean -ay


RUN pip install --upgrade pip && \
    pip install  -r requirements.txt

EXPOSE 5006
EXPOSE 80

# Go to dockerhub cli or use docker exec (docker exec -t -i interview:bokehapp /bin/bash)
# cd interview
# cd apps
# bokeh serve --allow-websocket-origin="*" --num-procs=4 (max no of processes) new.py

