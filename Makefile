slow:
	python -m src._slow.server 9000
M0:
	python -m src.M0.server 8000

M1:
	python -m src.M1.server 8000

M2:
	python -m src.M2.server 8000

M3:
	python -m src.M3.server 8000

echo:
	for i in 1 2 3; do ((echo 123 | nc localhost 8000)&); done
