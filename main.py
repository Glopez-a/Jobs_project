# Imports

import sys

from modules import streamlit as front
from modules import dbconection as conn



if __name__ == '__main__':
    
    df, conection = conn.connect()
    front.streamlit(df, conection)
    