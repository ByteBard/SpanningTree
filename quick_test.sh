#!/bin/bash

python3 run_spanning_tree.py TailTopo Tests/tail.txt
python3 run_spanning_tree.py ComplexLoopTopo Tests/complex.txt
python3 run_spanning_tree.py NoLoopTopo Tests/noloop.txt
python3 run_spanning_tree.py SimpleLoopTopo Tests/simple.txt


diff Tests/tail.txt Logs/TailTopo.log
diff Tests/complex.txt Logs/ComplexLoopTopo.log
diff Tests/noloop.txt Logs/NoLoopTopo.log
diff Tests/simple.txt Logs/SimpleLoopTopo.log