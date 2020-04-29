#Final Project 
Yanbo Shi
(This Project used some code from class materials.)

How to interact with my program?
There are two parts in my program.
1. Final_getdata_and_database.py is the file to scraping and crawling the data from websites and create a database to hold the data.
2. Final_data_display.py is using Flask and Plotly to display the data from database.

It takes more than 10 mins to run Final_getdata_and_database.py at the first time since the data is from thousands websites. I also used cashing in this project.

Here are the steps:
1. Run Final_getdata_and_database.py to get the database.
2. Run Final_data_display.py, and use a browser to visit 
http://127.0.0.1:5000
3. Follow the instructions on the web.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Python packages used:
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import re

import sqlite3
from flask import Flask, render_template, request
import plotly.graph_objects as go 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
note:
I did not push the cashing .json file since it is too large.