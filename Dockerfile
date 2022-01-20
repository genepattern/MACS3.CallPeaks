# Use an official Python runtime as a parent image
FROM python:3.8

# install numpy and MACS2

RUN pip install macs3==3.0.0a6

RUN mkdir /genepattern

COPY callpeak_cmd.py /genepattern/callpeak_cmd.py