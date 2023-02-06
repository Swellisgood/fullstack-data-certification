FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update

RUN curl -fsSL https://get.deta.dev/cli.sh | sh
RUN pip install openpyxl pandas gunicorn streamlit sklearn matplotlib seaborn plotly 

COPY . /home/app

CMD streamlit run --server.port $PORT app.py