. ./export_env.sh
if [ -z "$PORT" ]; then
    echo "ERROR: environment variable \$PORT not exists!"
    exit 1
fi
cd django_project
./manage.py migrate
nohup ./manage.py runserver 0.0.0.0:${PORT} > /dev/null &