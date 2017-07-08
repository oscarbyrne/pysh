Pysh
---

Pysh is a python interpreter that runs alongside your bash session.

Tired of writing ugly one-liners like this? yes you are
```bash
value=$(python -c "import json; print json.load(open('$fname'))['$key']")
```

yuck! With pysh you only ever have to open those resources once
```bash
source import-pysh
pysh import json
...
pysh file = open(fname)
pysh value = json.load(file)[key]
```

oh no you want to reverse an array...
```bash
arr=$(for (( idx=${#arr[@]}-1 ; idx>=0 ; idx-- )); do echo "${arr[idx]}"; done)
```

pysh to the rescue.
```bash
pysh arr.reverse()
```
oh my!


How it works
============
- bash converts state to json document and shoves it to python through the kernel
- python does its business and sends back a diff of what changed

Bugs / To do
============
- python interpreter
- mechanism for updating bash state
- IFS is showing up as ',' on python side
- python feed back to bash when it is ready for requests
