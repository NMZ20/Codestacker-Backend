
FROM python:3.8   

ENV DockerHOME=/home/app/webapp  


RUN mkdir -p $DockerHOME  

 
WORKDIR $DockerHOME  


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

 
COPY . $DockerHOME  
 
RUN pip install -r requirements.txt  
 
EXPOSE 8000  

RUN python manage.py makemigrations

RUN python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]