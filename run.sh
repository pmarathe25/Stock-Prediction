#!/bin/bash
xdg-open harambeinvestments.html
(lsof -i :8000 | grep python) | grep -v grep | awk '{print $2}' | xargs kill
python ./server.py &
