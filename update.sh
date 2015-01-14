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
