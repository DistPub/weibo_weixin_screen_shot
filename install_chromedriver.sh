# chrome web driver support
if [ ! -d "$HOME/chromedriver" ]; then
    wget http://chromedriver.storage.googleapis.com/2.9/chromedriver_linux64.zip -O /tmp/chromedriver_linux64.zip
    unzip /tmp/chromedriver_linux64.zip -d /tmp/
    mkdir -p $HOME/chromedriver/
    cp /tmp/chromedriver $HOME/chromedriver/
    chmod a+x $HOME/chromedriver/chromedriver
else
    echo 'Using cached chromedriver.';
fi

export PATH=$PATH:$HOME/chromedriver/