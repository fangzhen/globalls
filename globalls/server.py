#! /bin/python
import logging
import subprocess
import re
from urllib.parse import unquote, urlparse
from pygls.capabilities import *
from pygls.server import LanguageServer
from pygls.lsp import *
from pygls import uris

from globalls import utils

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

logger = logging
server = LanguageServer()


@server.feature(COMPLETION)
def completions(params: CompletionParams):
    """Returns completion items."""
    doc = server.lsp.workspace.get_document(params.textDocument.uri)
    token = doc.word_at_position(params.position)
    completions = utils.invoke_global(server, "-c %s" % token)
    return CompletionList(
        False,
        [CompletionItem(c) for c in completions])


def find_tag(params, global_args):
    doc = server.lsp.workspace.get_document(params.text_document.uri)
    tag = doc.word_at_position(params.position)
    defs = utils.invoke_global(
        server, "%s -a --color=always --result=grep %s" % (
            global_args, tag))
    locations = []
    for d in defs:
        items = d.split(":", 3)
        path = items[0]
        lineno = int(items[1]) - 1
        line = items[2]
        start_col = ANSI_ESCAPE.search(line).start()
        # It's not correct if tag is a regex, but good enough for common use
        end_col = start_col + len(tag)
        r = Range(start=Position(line=lineno, character=start_col),
                  end=Position(line=lineno, character=end_col))
        loc = Location(uri=uris.from_fs_path(path), range=r)
        locations.append(loc)

    return locations


@server.feature(DEFINITION)
def definition(params: DefinitionParams):
    """Find definitions."""
    return find_tag(params, "-d")


@server.feature(REFERENCES)
def reference(params: ReferenceParams):
    """Find references."""
    return find_tag(params, "-r")


@server.feature(TEXT_DOCUMENT_DID_SAVE)
def test_document_did_save(params: DidSaveTextDocumentParams):
    """Update global db when file saved."""
    path = uris.to_fs_path(params.textDocument.uri)
    utils.invoke_global(server, "--single-update %s" % path)


def main():
    server.start_io()


if __name__ == '__main__':
    main()
