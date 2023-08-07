FROM python:3.11 as python-base
WORKDIR /app
COPY /pyproject.toml /app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
ENV PYTHONPATH=/app:/app/src
EXPOSE 8080
CMD ["poetry", "run", "uvicorn", "src.chatbot.index:app", "--host", "0.0.0.0", "--port", "8080"]

