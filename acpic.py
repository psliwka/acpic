#!/usr/bin/env python3

import argparse
import logging
import os
import re
import socket
import subprocess
import time


logger = logging.getLogger("acpic")

xdg_config_home = os.environ.get("XDG_CONFIG_HOME") or os.path.join(
    os.environ["HOME"], ".config"
)
events_dir = os.path.join(xdg_config_home, "acpi", "events")


def rule_files():
    if not os.path.isdir(events_dir):
        logger.warning("Event handlers directory does not exist")
        return
    for filename in os.listdir(events_dir):
        if filename.startswith("."):
            continue
        filename = os.path.relpath(os.path.join(events_dir, filename))
        if os.path.isfile(filename):
            yield filename


def parse_rule(filename):
    logger.debug("Parsing file '%s'", filename)
    parsed_content = {}
    with open(filename) as datafile:
        for line in datafile:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = tuple(line.split("=", 1))
            parsed_content[key] = value
    logger.debug("Parsed content: %r", parsed_content)
    return parsed_content


def parsed_rules():
    for filename in rule_files():
        try:
            yield parse_rule(filename)
        except Exception as e:
            logger.error("Parsing file '%s' failed: %r", filename, e)


def rule_applicable(rule, event):
    match = re.search(rule["event"], event)
    if match is not None:
        logger.debug("Matched string: %s", match.group())
        return True
    else:
        return False


def event_actions(event):
    for rule in parsed_rules():
        if rule_applicable(rule, event):
            yield rule["action"]


def expand_action(action, event):
    def repl(match_object):
        expand_argument = match_object.group()[-1]
        if expand_argument == "e":
            return event
        else:
            return expand_argument

    return re.sub("%.", repl, action)


def run_action(action):
    logger.info("Calling: %s", action)
    try:
        output = subprocess.check_output(action, shell=True)
    except subprocess.CalledProcessError as e:
        logger.warning("Subprocess terminated with exit code %d", e.returncode)
        output = e.output
    if output:
        logger.debug("Subprocess stdout: %s", output)


def run_event_actions(event):
    for action in event_actions(event):
        run_action(expand_action(action, event))


def acpid_events():
    while True:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.connect("/var/run/acpid.socket")
        except Exception as e:
            logger.error("Could not connect to acpid socket: %r", e)
            logger.info("Retrying in one second...")
            time.sleep(1)
            continue
        logger.debug("Connected to acpid socket")
        for event in sock.makefile():
            logger.info("New event: %s", event.strip())
            yield event


def event_loop():
    try:
        for event in acpid_events():
            run_event_actions(event)
    except KeyboardInterrupt:
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Print what is being done"
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Print additional debug info (implies -v)",
    )
    return parser.parse_args()


def setup_logging(args):
    if args.debug:
        loglevel = logging.DEBUG
    elif args.verbose:
        loglevel = logging.INFO
    else:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)


def main():
    args = parse_args()
    setup_logging(args)
    event_loop()


if __name__ == "__main__":
    main()
