FROM python:3.8
LABEL authors="marcelochsendorf"


RUN apt update && apt upgrade -y && apt install -y libcairo2 libcairo2-dev libxt-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt



RUN pip install -e .

RUN python DisplayServer --install-completion bash


EXPOSE 5556


ENTRYPOINT ["DisplayServer"]
CMD ["DisplayServer", "--basepath", "./DisplayFramework/data", "launch"]