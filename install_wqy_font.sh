# chinese font support
wget http://mirror.0x.sg/debian/pool/main/f/fonts-wqy-zenhei/fonts-wqy-zenhei_0.9.45.orig.tar.gz -O /tmp/fonts-wqy-zenhei_0.9.45.orig.tar.gz
cd /tmp/
tar -xzvf fonts-wqy-zenhei_0.9.45.orig.tar.gz
cd wqy-zenhei
./configure --prefix=/usr && make && sudo make install