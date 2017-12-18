slow:
	python -m src._slow.server 9000
M0:
	python -m src.M0.server

M1:
	python -m src.M1.server

M2:
	python -m src.M2.server

M3:
	python -m src.M3.server

M4:
	python -msrc.M4.aevent src/M4/server.py

echo:
	for i in 1 2 3; do ((echo 123 | nc localhost 8000)&); done
