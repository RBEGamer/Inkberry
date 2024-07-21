FROM python:3.8
LABEL authors="marcelochsendorf"


RUN apt update && apt upgrade -y && apt install -y libcairo2 libcairo2-dev libxt-dev libmagickwand-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt






EXPOSE 55556

RUN pip install -e .
#RUN DisplayServer --install-completion bash
RUN DisplayServer --help

ENTRYPOINT ["DisplayServer"]
CMD ["launch" , ""]