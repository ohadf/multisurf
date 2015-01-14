wget http://python.org/ftp/python/2.7.6/Python-2.7.6.tgz
tar -xzvf Python-2.7.6.tgz
cd Python-2.7.6
yes | sudo yum erase python
./configure --prefix=/usr --enable-unicode=ucs4 --enable-shared LDFLAGS="-Wl,-rpath /usr/lib"
make
sudo make install
cd ..
wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo pip install -U pip
sudo pip install paramiko

