FROM ubuntu:20.04 as geoid-downloader

# Does this work?
RUN apt-get update && apt-get install -y geographiclib-tools
RUN geographiclib-get-geoids egm96-5 

# RUN apt-get update && apt-get install -y software-properties-common
# RUN add-apt-repository universe && apt-get update && apt-get install -y geographiclib-tools



FROM python:3.8-bullseye

COPY --from=geoid-downloader /usr/share/GeographicLib/geoids /usr/share/GeographicLib/geoids
COPY . /python-droneresponse-mathtools/
WORKDIR /python-droneresponse-mathtools/
RUN pip install .