. ./export_env.sh
pip install -r requirements.txt
cd django_project
./manage.py migrate
cd ..