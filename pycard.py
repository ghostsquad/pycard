from jinja2 import Template
import os
import sys
import time
import logging
import csv
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
from itertools import zip_longest
from livereload import Server, shell

csv.register_dialect('pipes', delimiter='|')

RENDERED_CARDS_FILE = "index.html"


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class CardRenderer:
    def __init__(self, input_path):
        self.single_card_template_path = os.path.join(input_path, "_card.html.jinja2")
        self.csv_card_path = os.path.join(input_path, "_card.csv")
        self.cards_template_path = os.path.join(os.path.dirname(__file__), 'cards.html.jinja2')
        self.all_cards_rendered_path = os.path.join(input_path, RENDERED_CARDS_FILE)

    def render_cards(self):
        # load the csv file
        cards_data = csv.DictReader(open(self.csv_card_path), dialect='pipes')

        rendered_cards = []

        # load the single card template
        with open(self.single_card_template_path, "r") as template_file:
            template = Template(template_file.read())

            # render the template with card data
            for card_data in cards_data:
                rendered_cards.append(template.render(card_data))

        # group cards into columns of 4
        cards_grouped = grouper(rendered_cards, 4)

        # render the cards template with all rendered cards
        with open(self.cards_template_path, "r") as cards_template_file:
            template = Template(cards_template_file.read())

            with open(self.all_cards_rendered_path, "w") as all_cards_rendered_file:
                all_cards_rendered_file.write(template.render(cards_grouped=cards_grouped))


class RenderingEventHandler(FileSystemEventHandler):
    def __init__(self, card_renderer):
        self.card_renderer = card_renderer

    def on_any_event(self, event):
        if event.src_path == self.card_renderer.all_cards_rendered_path:
            return

        self.card_renderer.render_cards()


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    card_renderer = CardRenderer(path)

    observer = Observer()
    observer.schedule(LoggingEventHandler(), path, recursive=True)
    observer.schedule(RenderingEventHandler(card_renderer), path, recursive=True)
    observer.start()

    card_renderer.render_cards()

    server = Server()
    server.watch(os.path.join(path, RENDERED_CARDS_FILE))
    server.serve(root=path)

    observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
