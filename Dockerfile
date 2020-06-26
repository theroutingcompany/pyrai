FROM jupyter/datascience-notebook:latest
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
COPY . .
RUN pip install --upgrade pip && \
    pip install -e .
WORKDIR $HOME