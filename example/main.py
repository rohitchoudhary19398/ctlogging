import time
from ctlogging.config import set_logger_from_yaml, addLoggingLevel
from ctlogging.context import correlation_id
from uuid import uuid4

addLoggingLevel("SUBDEBUG", 15)


class Pipeline:
    def __init__(self, yamlfilepath: str = None):
        self.logger = set_logger_from_yaml(yamlfilepath=yamlfilepath)

    def f1(self):
        time.sleep(1)
        self.logger.subdebug("in f1 function")

    def f2(self, uuid):
        correlation_id.set(uuid4().hex)
        self.logger.info("f1 call start")
        self.f1()
        self.logger.info("f1 call end")


if __name__ == "__main__":
    lf = r"example/log.yaml"
    de = Pipeline(lf)
    de.f2("Sd")
