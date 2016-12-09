#!/bin/bash
BROWSER=$(gconftool -g /desktop/gnome/url-handlers/http/command)
export BROWSER="${BROWSER//"\"%s\""/}"
python ./server.py &
sensible-browser harambeinvestments1.html
