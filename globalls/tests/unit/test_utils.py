import os
import unittest

import pygls.types

from globalls import utils


class TestUtils(unittest.TestCase):
    def test_find_token_at_position(self):
        params = pygls.types.CompletionParams(
            pygls.types.TextDocumentIdentifier(
                "file://%s/demosrc" % os.path.dirname(
                    os.path.abspath(__file__))),
            pygls.types.Position(3, 6),
            pygls.types.CompletionContext(None, None),
        )
        t = utils.find_token_at_position(params)
        self.assertEqual(t, 'abcd')

    def test_find_token_before_position(self):
        params = pygls.types.CompletionParams(
            pygls.types.TextDocumentIdentifier(
                "file://%s/demosrc" % os.path.dirname(
                    os.path.abspath(__file__))),
            pygls.types.Position(3, 8),
            pygls.types.CompletionContext(None, None),
        )
        t = utils.find_token_at_position(params, before=True)
        self.assertEqual(t, 'abcd')
