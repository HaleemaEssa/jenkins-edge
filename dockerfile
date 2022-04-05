FROM python:3
WORKDIR /usr/app/
COPY . .
#########
#########
RUN apt-get clean
##########
RUN python3 -m pip install pika --upgrade
RUN pip3 install pandas
#CMD ["r.py"]
#COPY data.csv .
#CMD ["rnhbooth.py"]
#CMD ["rnhbth.py"]
#CMD ["arr.py"]
#CMD ["onec.py"]
#CMD ["msg.py"]
##CMD ["msght.py"]
#CMD ["msght1.py"]
#CMD ["aprod1.py"]
#CMD ["booth.py"]
##ENTRYPOINT ["python3"]






CMD ["pe1.py"]
ENTRYPOINT ["python3"]




########
#######






# RUN python3 -m pip install pika --upgrade
## RUN apt-get clean
##RUN apt-get update -y
# RUN apt-get -oDebug::pkgAcquire::Worker=1 update
# RUN python3 -m pip install --upgrade pip setuptools wheel                                                                                                                                                                                                
# RUN apt-get update --allow-unauthenticated -y
## CMD ["p.py"]
## ENTRYPOINT ["python3"]
