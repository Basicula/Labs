@echo off
	python -m pip install --upgrade pip
echo installing PrettyTable
	pip install prettytable
echo installed PrettyTable
echo Running app
	python generation.py
	
pause