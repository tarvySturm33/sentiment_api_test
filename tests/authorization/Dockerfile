FROM python:3.12-slim
ADD requirements.txt /tests/requirements.txt
ADD test_authorization.py /tests/test_authorization.py
WORKDIR /tests/
RUN pip install --no-cache-dir -r requirements.txt
CMD python3 test_authorization.py
