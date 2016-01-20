# chrome web driver support
wget http://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo cp chromedriver /usr/local/bin/
sudo chmod a+x /usr/local/bin/chromedriver

# chinese font support
sudo apt-get install fonts-wqy-zenhei

# fake x server
sudo apt-get install xvfb

# export DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE="django_project.settings"