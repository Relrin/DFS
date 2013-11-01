mkdir C:\Code\CSaN\data
mkdir C:\Code\CSaN\data\fs1
mkdir C:\Code\CSaN\data\fs2
start python fileserver.py 127.0.0.1 5001 fs1
start python fileserver.py 127.0.0.1 5002 fs2
start python server.py 2
