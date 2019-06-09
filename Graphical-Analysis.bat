:: Must execute inside Payload's Library
@echo off
SET dot="C:\Program Files (x86)\Graphviz2.38\bin\dot.exe"
cd ..
python -m cProfile -o .\Payload\Payload.pstats Payload\__main__.py
python -m gprof2dot --show-samples -f pstats .\Payload\Payload.pstats | %dot% -Tsvg -Gcenter=1 -Gclusterrank="local" -Gnormalize=1 -Noverlap=0 -Nshape="rect" -Earrowhead="onormal" -Etail="box" -o .\Payload\Visualization.svg -s
cd Payload

