# 
FROM python:3.10

#
EXPOSE 8501

# 
WORKDIR /container

# 
COPY ./requirements.txt /container/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /container/requirements.txt

# 
COPY ./app /container/app

#
WORKDIR /container/app

# 
ENTRYPOINT ["streamlit", "run","convene_ecommerce.py", "--server.port=8501", "--server.address=0.0.0.0"]
# docker build -t example_docker_servvice .
# Behind a TLS Termination Proxy¶
# If you are running your container behind a TLS Termination Proxy (load balancer) like Nginx or Traefik, add the option --proxy-headers, this will tell Uvicorn to trust the headers sent by that proxy telling it that the application is running behind HTTPS, etc.
# docker run -d --name mycontainer -p 80:80 example_docker_service