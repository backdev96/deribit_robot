FROM python:3.9
LABEL author='Stas Efremov, stasefremovx@gmail.com'
RUN mkdir /code
RUN pip install poetry 'poetry==1.0.0'
COPY . .
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction
CMD python robot.py
