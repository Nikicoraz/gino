import re
pattern = r'[a-zA-Z]+'
t = re.findall(pattern, 'ciao9gio09023ff')
print(t)