FROM continuumio/anaconda3
MAINTAINER Benjamin Klepper

RUN conda env create -f environment.lock.yml
RUN source activate interactive_app
RUN cd interactive_app
RUN python setup.py develop
RUN cd ..
EXPOSE 5006
CMD ./run.sh
