FROM python:3.11.1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip freeze 

COPY . .

CMD ["python", "main.py", "--deaf", "--silent"]
