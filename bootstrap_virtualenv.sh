. ./export_env.sh

# ubuntu packages support
. ./ubuntu_requirements.sh

# virtualenv support
sudo pip install virtualenv

cd ..
# create virtualenv
virtualenv weibo_weixin_screen_shot_env

# active virtualenv
. ./weibo_weixin_screen_shot_env/bin/activate

cd weibo_weixin_screen_shot
# python package support
pip install -r requirements.txt

# chrome web driver support
. ./install_chromedriver.sh