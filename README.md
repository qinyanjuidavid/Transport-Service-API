# Transport-Service-API
### Steps to install and run in local system 🚀
- Create a virtual environment `python -m venv <env_name>`
- Activate virtual environment `source <env_name>/bin/activate`
- Install requirements in venv `pip install -r requirements.txt`
- Ensure you have GDAL and postgresql installed locally on your machine
- Make migrations `python manage.py makemigrations --settings=src.settings.development`
- Apply migrations `python manage.py migrate --settings=src.settings.development`
- Create a super user `python manage.py createsuperuser --settings=src.settings.development`
- Run the server `python manage.py runserver --settings=src.settings.development`

### Testing
> I used coverage as my test reporting tool
- coverage run manage.py test
- coverage html
- coverage report


