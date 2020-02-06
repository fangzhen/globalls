#! /bin/python
import logging
import subprocess
import re

import pygls.uris

TOKEN_REG = r'\b[a-zA-Z_]\w*\b'

logging.basicConfig(level=logging.DEBUG)
logger = logging


def find_token_at_position(params, before=False):
    path = pygls.uris.to_fs_path(params.textDocument.uri)
    lineno = params.position.line
    colno = params.position.character
    if before:
        colno -= 1
    with open(path) as src:
        lines = src.readlines()
        line = lines[lineno]
        for m in re.finditer(TOKEN_REG, line):
            if m.start() <= colno and m.end() > colno:
                return m[0]


def invoke_global(server, params):
    """Invoke `global` with specified parameters and return output"""
    try:
        cmd = 'global %s' % params
        logging.debug('Executing: %s' % cmd)
        p = subprocess.Popen(cmd,
                             cwd=server.lsp.workspace.root_path,
                             shell=True, stdout=subprocess.PIPE,
                             text=True)
        output = p.stdout.read().splitlines()
    except OSError:
        logger.exception('Failed to invoke global')
        output = ''

    logging.debug("Got output from global: %s" % output)
    return output
