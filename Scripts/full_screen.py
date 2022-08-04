import numpy as np
import pandas as pd
import pandas.io.sql as sql
import pymysql
import thefuzz
import xlwt
import sqlalchemy
import time
import civitatisAPI as civi
import requests
import json

from requests.auth import HTTPBasicAuth
from thefuzz import fuzz
from thefuzz import process
from sqlalchemy import create_engine
from pymysql import*
from IPython.display import clear_output