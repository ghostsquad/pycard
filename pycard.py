from jinja2 import Template
import os
from optparse import OptionParser
import logging
import csv
import time
import re
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from itertools import zip_longest
from livereload import Server


VERSION = '0.1.0'

RENDERED_CARDS_FILE = "index.html"


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class CardRenderer:
    def __init__(self, input_path, prefix):
        self.prefix = prefix

        self.single_card_template_path = os.path.join(input_path, "{}.html.jinja2".format(prefix))
        self.csv_card_path = os.path.join(input_path, "{}.csv".format(prefix))
        self.cards_template_path = os.path.join(os.path.dirname(__file__), 'cards.html.jinja2')
        self.all_cards_rendered_path = os.path.join(input_path, RENDERED_CARDS_FILE)

    def render_cards(self):
        # I've noticed that when saving the CSV file
        # the server reloads an empty page
        # unless I add a small sleep before attempting to read everything
        time.sleep(0.5)

        # load the csv file
        cards_data = []
        with open(self.csv_card_path, "r", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, dialect='custom_delimiter')
            for row in reader:
                cards_data.append(row)

        rendered_cards = []

        # load the single card template
        with open(self.single_card_template_path, "r") as template_file:
            template = Template(template_file.read())

            # render the template with card data
            for card_data in cards_data:
                rendered = template.render(card_data)
                num_cards = card_data.get('num_cards', 1)
                if num_cards is None or re.match("^[^0-9]*$", num_cards):
                    num_cards = 1

                num_cards = int(num_cards)
                for i in range(0, int(num_cards)):
                    rendered_cards.append(rendered)

        # group cards into columns of 4
        cards_grouped = grouper(rendered_cards, 4)

        # render the cards template with all rendered cards
        with open(self.cards_template_path, "r") as cards_template_file:
            template = Template(cards_template_file.read())
            with open(self.all_cards_rendered_path, "w") as all_cards_rendered_file:
                all_cards_rendered_file.write(template.render(cards_grouped=cards_grouped, prefix=self.prefix))


class RenderingEventHandler(FileSystemEventHandler):
    def __init__(self, card_renderer):
        self.card_renderer = card_renderer

    def on_any_event(self, event):
        if event.src_path == self.card_renderer.all_cards_rendered_path:
            return

        self.card_renderer.render_cards()


def parse_options():
    parser = OptionParser(
        usage="usage: %prog [options]",
        version="%prog {}".format(VERSION)
    )
    parser.add_option("-p", "--path",
                      help="path to assets",
                      dest="path",
                      default=os.getcwd(),
                      metavar="PATH")

    parser.add_option("-x", "--prefix",
                      help="filename prefix, example _card<.ext>",
                      dest="prefix",
                      default="_card",
                      metavar="PREFIX")

    parser.add_option("-d", "--delimiter",
                      help="delimiter used in the csv file, default: , (comma)",
                      dest="delimiter",
                      default=",",
                      metavar="DELIMITER")

    parser.add_option("--port",
                      help="port to use for live reloaded page",
                      dest="port",
                      type="int",
                      default=8800,
                      metavar="PORT")

    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    (options, args) = parse_options()

    port = options.port
    assets_path = options.path
    file_prefix = options.prefix

    csv.register_dialect('custom_delimiter', delimiter=options.delimiter)

    card_renderer = CardRenderer(assets_path, file_prefix)

    observer = Observer()
    observer.schedule(LoggingEventHandler(), assets_path, recursive=True)
    observer.schedule(RenderingEventHandler(card_renderer), assets_path, recursive=True)

    card_renderer.render_cards()

    observer.start()

    server = Server()
    server.watch(card_renderer.all_cards_rendered_path)
    server.serve(root=assets_path, port=port, host='0.0.0.0')

    observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
