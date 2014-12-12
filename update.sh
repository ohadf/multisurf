sudo yum update
yes | sudo yum install make automake gcc gcc-c++ kernel-devel
yes | sudo yum groupinstall “Development tools”
yes | sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
wget http://ftp.gnu.org/gnu/tar/tar-1.28.tar.gz
tar -xzvf tar-1.28.tar.gz
cd tar-1.28
./configure
make
sudo make install
cd ..
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

