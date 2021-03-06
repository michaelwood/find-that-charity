import logging

from ftc.models import Scrape


class ScrapeHandler(logging.StreamHandler):
    def __init__(self, scrape):
        logging.StreamHandler.__init__(self)
        self.scrape = scrape

    def emit(self, record):
        msg = self.format(record)
        self.scrape.log += msg + "\n"
        if record.levelno in (logging.WARNING, logging.ERROR, logging.CRITICAL):
            self.scrape.errors += 1
        self.scrape.save()

    def teardown(self):
        if self.scrape.items == 0:
            self.scrape.status = Scrape.ScrapeStatus.FAILED
        elif self.scrape.errors > 0:
            self.scrape.status = Scrape.ScrapeStatus.ERRORS
        else:
            self.scrape.status = Scrape.ScrapeStatus.SUCCESS
        self.scrape.save()
