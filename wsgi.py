import socket
from flask import Flask

import datetime


application = Flask(__name__)


def write_into_log():
    with open("/mnt/logs/log.txt", "a") as f:
        f.write(
            "%s: Request processed by %s" %
            (datetime.datetime.now(), socket.gethostname())
        )

    return True


def get_log():
    try:
        with open("/mnt/logs/log.txt", "r") as f:
            return f.read()[-5000:]
    except IOError:
        return (
            "No log exists. This shouldn't happen since we write into the log"
            " before reading it"
        )


@application.route("/")
def hello():
    write_into_log()
    log = get_log()

    message = "Hello world from %s" % socket.gethostname()

    return (
        """
        <html>
            <head>
                <title>Hello World</title>
            </head>
            <body>
                <h1>{message}</h1>
                <p>And here is the log:</p>
                <pre>
                    {log}
                </pre>
            </body>
        </html>
        """.format(message=message, log=log)
    )


if __name__ == "__main__":
    application.run()
