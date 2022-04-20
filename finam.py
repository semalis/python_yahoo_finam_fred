import re
import urllib.request

f = urllib.request.urlopen("http://www.finam.ru/cache/icharts/icharts.js")
lines = f.readlines()

for line in lines:
    m = re.match('var\s+(\w+)\s*=\s*\[\\s*(.+)\s*\]\;',  line.decode('windows-1251'))
    if m is not None:
        varname = m.group(1)
        if varname == "aEmitentIds":
            aEmitentIds = line #its type is 'bytes', not 'string'