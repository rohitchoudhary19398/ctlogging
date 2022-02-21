# Ctlogging

Middleware for loading or generating correlation IDs for each run. Correlation IDs can be added to your logs, making it simple to retrieve all logs generated from a single run.

It also help in logging message in mysql database

When the process starts a correlation ID is set in the contextvar and retrieve using the filter during logging and inject into log record.


## 1. How to install

Using pip
 
`pip install ctlogging`

Using poetry
 
`poetry ctlogging`


## 2. How to use
There are main three step requires -

* Initalize the logger at starting point of application 
  ```
  from ctlogging.config import set_logger_from_yaml, set_logger

  logger = set_logger_from_yaml(logconfig_yaml) # using file
  logger = set_logger(config) # using dict
  ```  

* get logger at module/file level and start logging using logger built-in method
  ```
  from ctlogging.config import get_logger

  logger = get_logger(__name__)
  logger.info(message...)
  logger.debug(message...)
  ```

* for correlation_id, set it at entry level of pipeline 
  ```
  from uuid import uuid4
  from ctlogging.context import correlation_id

  def pipeline():
      uid = uuid4().hex
      correlation_id.set(uid) # uid is string
      "do task....."
  ```

## 3. Configuration
using config.yaml file
```
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(correlation_id)s - %(levelname)s - %(name)s - %(message)s'
filters:
  correlation_id:
    (): ctlogging.CorrelationId
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    filters: [correlation_id]
    stream: ext://sys.stdout
  file:
    class : logging.handlers.RotatingFileHandler
    formatter: simple
    filename: extraction.log
    maxBytes: 3000000
    backupCount: 3
    filters: [correlation_id]
  db:
    class : ctlogging.MysqlHandler
    level: DEBUG
    host: localhost
    database: ares
    user: root
    password: root
    port: 3306
loggers:
  root:
    level: DEBUG
    handlers: [console, db]
    propagate: true
root_logger_name: root
```

## 3. for Developement
Steps: -
1. git clone the repo
2. install poetry from `https://python-poetry.org/docs/master/#installing-with-the-official-installer`
3. goto `ctlogging` directory
4. poetry install






