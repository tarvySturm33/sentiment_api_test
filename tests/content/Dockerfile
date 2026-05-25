FROM python:3.12-slim
ADD requirements.txt /tests/requirements.txt
ADD test_content.py /tests/test_content.py
WORKDIR /tests/
RUN pip install --no-cache-dir -r requirements.txt
CMD python3 test_content.py
