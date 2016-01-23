if [ -z "$PORT" ]; then
    echo "ERROR: environment variable \$PORT not exists!"
    exit 1
fi
ps axf|grep runserver|grep ${PORT}|grep -v grep|awk '{print " " $1}'|xargs kill -9