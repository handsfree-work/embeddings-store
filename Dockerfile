#FROM registry.cn-shenzhen.aliyuncs.com/handsfree/node:18 AS admin_client
#WORKDIR /work
#ADD ./frontend/admin/package.json ./package.json
#RUN npm install -g pnpm
#RUN pnpm install
#
#ADD ./frontend/admin/ .
#RUN npm run build

# Pull official latest Python Docker image (Pulished with version 3.11.0)
FROM --platform=linux/amd64 registry.cn-shenzhen.aliyuncs.com/handsfree/python:3.10

# Set the working directory
WORKDIR /usr/backend

# Set up Python behaviour
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/venv

# Switch on virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# Set the server port
EXPOSE 8006

# Install system dependencies
#RUN apt-get update \
#  && apt-get -y install netcat gcc postgresql \
#  && apt-get clean
#ENV HTTPS_PROXY=http://192.168.34.139:10811
# Install Python dependencies
RUN pip install --upgrade pip
COPY ./backend/requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy all files
COPY ./backend/ .
# Copy entrypoint.sh for auto connection with account_db service
#COPY ./backend/entrypoint.sh .
RUN chmod +x /usr/backend/entrypoint.sh


# 将编译好的前端文件复制到public文件夹下
#COPY --from=admin_client ./dist/ ./public/
ADD ./frontend/admin/dist/ ./public/
# Execute entrypoint.sh
ENTRYPOINT ["/usr/backend/entrypoint.sh" ]

ENV basic_server_host 0.0.0.0
ENV basic_server_port 8006
ENV basic_server_works 4
# Start up the backend server
CMD uvicorn src.main:backend_app --host $basic_server_host --port $basic_server_port
