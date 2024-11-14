# Data Provider
## Getting Started
Make sure Docker is installed on your machine. If not, please follow the instructions [here](https://docs.docker.com/get-docker/).
Also Github CLI is required to fork the repository. If not installed, please follow the instructions [here](https://cli.github.com/manual/installation).
```bash
gh repo fork --clone=true https://github.com/dax1216/blankon_dashboard.git
brew install pyenv pyenv-virtualenv
pyenv init  # append the output to your .zshrc and restart your shell
pyenv install 3.12.2
pyenv virtualenv 3.12.2 blankon_dashboard-py3.12.2
pyenv activate blankon_dashboard-py3.12.2  # do this every time you start working on this project
cp env-sample .env
pip install -r requirements.txt
docker compose down --volumes && docker compose up -d
```
## Contributing
* Make sure to create a copy of .env-sample and rename to .env

## Basic Commands
### Create superuser (optional)
```bash
docker exec -it blankon_dashboard-django-1 bash
python manage.py createsuperuser
```
### Import data sample (optional)
```bash
docker exec -it blankon_dashboard-django-1 bash
python manage.py runscript apps.dashboard.import_data
```
### Run linting, flake8, and isort
```bash
pre-commit install
pre-commit run --all-files
```
## Using the app
* Open your browser and go to http://localhost:8000/api/v1/schema/swagger/
* Test existing endpoints
