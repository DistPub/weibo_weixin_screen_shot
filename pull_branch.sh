if [ -z "$BRANCH" ]; then
    echo "ERROR: environment variable \$BRANCH not exists!"
    exit 1
fi
git fetch origin
git reset --hard origin/${BRANCH}