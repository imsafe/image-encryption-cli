# Image Encryption CLI

Dependency installation.

$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt

Encryption:
$ python3 main.py enc -i <inputfile> -o <outputfile> -p <password>

Decryption:
$ python3 main.py dec -i <inputfile> -o <outputfile> -p <password>

Help:
python3 main.py --help