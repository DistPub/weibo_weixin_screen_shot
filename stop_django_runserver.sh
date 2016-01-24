if [ -z "$PORT" ]; then
    echo "ERROR: environment variable \$PORT not exists!"
    exit 1
fi
kill -9 $(ps axf|grep runserver|grep ${PORT}|grep -v grep|awk '{print $1}')
kill -9 $(lsof -ti:${PORT})