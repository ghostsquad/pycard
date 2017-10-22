# PyCard
Un-opinionated card game prototyping engine

Generate printable cards for prototyping using csv, html, css.

* Card data stored in csv file (delimiter can be specified)
* Html jinja2 templating
* CSS for styling

_Only tested in Python 3.6_

###  Quick Start

```
git clone https://github.com/ghostsquad/pycard.git
cd pycard
pip install -r requirements.txt
python pycard.py -p ./examples -d "|"
```

OR

```
docker run -p 8800:80 ghostsquad/pycard pycard -p ./examples -d "|"
```

Running the Docker container with your own data (comma separated csv)

```
docker run -p80 -v /path/to/your/card_files:/data ghostsquad/pycard pycard -p /data -d ","
```

Example output

```
$ python pycard.py examples
[I 171010 19:30:34 server:283] Serving on http://127.0.0.1:8800
2017-10-10 19:30:34 - Serving on http://127.0.0.1:8800
[I 171010 19:30:34 handlers:60] Start watching changes
2017-10-10 19:30:34 - Start watching changes
[I 171010 19:30:34 handlers:62] Start detecting changes
2017-10-10 19:30:34 - Start detecting changes
2017-10-10 19:30:34 - Created file: examples/index.html
2017-10-10 19:30:34 - Modified directory: examples
```

Navigate to `localhost:8800` to see your cards. This page will automatically refresh anytime changes are made.

You can also run `python pycard.py --help` for a list of options.

See `examples` directory to setup your files

### Explanation

Required files in a directory:

```
examples
├── _card.css
├── _card.csv
├── _card.html.jinja2
```
Note: You can change the prefix with the `-x` or `--prefix` commandline option. Default is `_card`.

Optional files:

* `_card.header.html` - Add custom header to the final index.html file.

```diff
- Important
index.html file is created/overwritten in the assets path!
```

* `_card.csv` is your data. Column names become variables to be used in `_card.html.jinja2`

    * `num_cards` is a special column name. You can use this to indicate how many copies of a particular card will be rendered.

      When this column is missing or has a non-numeric value, it defaults to 1 card.
      Using 0 is the column will cause the card not to be rendered.
      This is useful if you have a card idea, but aren't ready yet to print it for prototyping.

    * `ignore` is a special column name. You can use this to prevent a row from being rendered.
      I've found this useful to ignore the row with card count sums.

* `_card.css` is your styling. This will be automatically loaded. As your cards will be printed, be careful to use physical units (mm, pt...) instead of pixels to define dimensions.
* `_card.html.jinja2` will be your html template. See [Jinja Documentation](http://jinja.pocoo.org/docs/2.9/templates/) for details.

The page found at localhost:8800 is now printable!

![image](https://user-images.githubusercontent.com/903488/31474239-521061be-aeae-11e7-81ac-626490faacee.png)

### Credits

Inspired by https://github.com/vaemendis/hccd
