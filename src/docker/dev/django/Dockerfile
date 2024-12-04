# 031224, Tuesday, 04.00 pm 
# 1. Build Dependecy Wheels 
# 2. RUN Application 


ARG PYTHON_VERSION=3.10-bullseye
FROM python:${PYTHON_VERSION} AS python 

# 1. Python Dependency Wheels | Build Stage 1 
FROM python AS python-build-stage
ARG BUILD_ENVIRONMENT=dev

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev 

COPY ./requirements . 

RUN pip wheel --wheel-dir /usr/src/app/wheel \
        -r ${BUILD_ENVIRONMENT}.txt 

# Run Application | Build Stage 2
FROM python AS python-run-stage 

RUN addgroup --system todoapp && adduser --system --ingroup todoapp todoapp 

ARG BUILD_ENVIRONMENT=dev
ARG APP_HOME=/home/todoapp/app 

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

#  ${APP_HOME}/vod-media-files is the External volume mount point. See docker compose file for the mount point. 
RUN mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles  && \
        chown -R todoapp:todoapp ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles && \
        chmod -R 775 ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles 


RUN apt-get update && apt-get install --no-install-recommends -y \
        libpq-dev \
        gettext \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheel /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/ 

COPY --chown=todoapp:todoapp ./docker/dev/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --chown=todoapp:todoapp ./docker/dev/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY --chown=todoapp:todoapp . ${APP_HOME} 
RUN chown todoapp:todoapp ${APP_HOME} 
USER todoapp

ENTRYPOINT ["/entrypoint.sh"]