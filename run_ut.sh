. ./export_env.sh
cd django_project
coverage run --source='.' ./manage.py test --pattern="tests_*.py"
coverage html