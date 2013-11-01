mkdir C:\Code\CSaN\data
mkdir C:\Code\CSaN\data\fs1
mkdir C:\Code\CSaN\data\fs2
mkdir C:\Code\CSaN\data\fs3
mkdir C:\Code\CSaN\data\fs4
start python fileserver.py 127.0.0.1 5001 fs1
start python fileserver.py 127.0.0.1 5002 fs2
start python fileserver.py 127.0.0.1 5003 fs3
start python fileserver.py 127.0.0.1 5004 fs4
start python server.py 4
