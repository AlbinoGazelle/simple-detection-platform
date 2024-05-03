# grab python base image
FROM python:3.12-slim

# Move to the app directory
WORKDIR /app

# Copy everything into app
COPY . /app

# Install everything from requirements.txt
RUN pip install -r requirements.txt

# Make streamlit port available
EXPOSE 8501

# Start our app
ENTRYPOINT ["streamlit", "run", "app/src/Overview.py"]