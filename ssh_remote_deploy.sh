if [[ $TRAVIS_BRANCH == 'master' ]]; then
    echo "Deploy production..."
    sshpass -e ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST cd $DEPLOY_HOME/production/weibo_weixin_screen_shot && ./deploy_production.sh
fi
if [[ $TRAVIS_BRANCH == 'develop' ]]; then
    echo "Deploy Staging..."
    sshpass -e ssh -o StrictHostKeyChecking=no $DEPLOY_USER@$DEPLOY_HOST cd $DEPLOY_HOME/staging/weibo_weixin_screen_shot && ./deploy_staging.sh
fi