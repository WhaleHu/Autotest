import json
import re
import os
import shutil
import sys
import time
import yaml

with open('setting.yaml', 'r') as f:
    set= yaml.load(f)
    print(set)