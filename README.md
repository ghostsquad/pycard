# pycard
Opinionated card game prototyping engine

Generate printable cards for prototyping using csv, html, css.

* Card data stored in csv/tsv
* Html jinja2 templating
* CSS for styling

_Only tested in Python 3.6_

# Quick Start

See `examples` directory to setup your files

```
$ python pycard.py examples
[I 171010 19:30:34 server:283] Serving on http://127.0.0.1:5500
2017-10-10 19:30:34 - Serving on http://127.0.0.1:5500
[I 171010 19:30:34 handlers:60] Start watching changes
2017-10-10 19:30:34 - Start watching changes
[I 171010 19:30:34 handlers:62] Start detecting changes
2017-10-10 19:30:34 - Start detecting changes
2017-10-10 19:30:34 - Created file: examples/index.html
2017-10-10 19:30:34 - Modified directory: examples
```

Inspired by https://github.com/vaemendis/hccd
