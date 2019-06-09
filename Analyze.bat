:: Must execute inside Payload's Library
@echo off
cd ..
python -m cProfile Payload\__main__.py
cd Payload