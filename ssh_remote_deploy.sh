if [[ $TRAVIS_BRANCH == 'master' ]]; then
    echo "Deploy production..."
    sshpass -e ssh $DEPLOY_USER@$DEPLOY_HOST ~/production/weibo_weixin_screen_shot/deploy_production.sh
fi
if [[ $TRAVIS_BRANCH == 'develop' ]]; then
    echo "Deploy Staging..."
    sshpass -e ssh $DEPLOY_USER@$DEPLOY_HOST ~/staging/weibo_weixin_screen_shot/deploy_staging.sh
fi