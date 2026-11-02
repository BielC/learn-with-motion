"""Offline checks of input boundaries, alignment and sharing safeguards."""

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qwen = load('qwen', 'scripts/qwen_narration.py')
package = load('package', 'tools/check_package.py')


class NarrationTests(unittest.TestCase):
    def test_duplicate_and_path_ids_rejected(self):
        examples = [[{'id': '../outside', 'text': 'Hello.'}],
                    [{'id': 'same', 'text': 'First.'}, {'id': 'same', 'text': 'Second.'}]]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'script.json'
            for cues in examples:
                path.write_text(json.dumps(cues))
                with self.assertRaises(ValueError):
                    qwen.load_cues(path)

    def test_sample_preserves_paragraph(self):
        cues = qwen.load_cues(ROOT / 'examples/narration.json', limit=1)
        self.assertEqual(len(cues), 1)
        self.assertGreater(len(cues[0]['text'].split('. ')), 2)

    def test_alignment_preserves_known_text_and_word_times(self):
        text = 'The request succeeds. The reply is lost.'
        words = [{'word': w, 'start': i * .5, 'end': i * .5 + .4}
                 for i, w in enumerate(text.split())]
        sentences, agreement = qwen.align(text, words, 5)
        self.assertEqual([s['text'] for s in sentences], ['The request succeeds.', 'The reply is lost.'])
        self.assertEqual(agreement['agreement'], 1)
        self.assertEqual(sentences[1]['start'], 1.5)
        self.assertTrue(all(a['end'] < b['start'] for a, b in zip(sentences, sentences[1:])))

    def test_low_agreement_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Low speech/script agreement'):
            qwen.align('The original operation already succeeded.',
                       [{'word': 'Unrelated', 'start': 0, 'end': 1}], 2)

    def test_model_fingerprint_changes_with_weights(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)
            (path / 'config.json').write_text('{}')
            (path / 'weights.safetensors').write_bytes(b'first')
            before = qwen.model_identity(path)
            (path / 'weights.safetensors').write_bytes(b'other')
            self.assertNotEqual(before, qwen.model_identity(path))

    def test_numeric_normalization(self):
        self.assertEqual(qwen.canonical('0.8'), qwen.canonical('point eight'))
        self.assertEqual(qwen.canonical('128'), qwen.canonical('one hundred twenty eight'))


class SharingTests(unittest.TestCase):
    def test_unexpected_media_rejected(self):
        self.assertIn('unexpected distribution file', package.inspect_contents('lesson.mp4', b'not a movie\n'))

    def test_credential_match_is_reported_without_value(self):
        synthetic = 'gh' + 'p_' + 'x' * 40
        findings = package.inspect_contents('README.md', (synthetic + '\n').encode())
        self.assertIn('GitHub credential', findings)
        self.assertNotIn(synthetic, ' '.join(findings))

    def test_home_path_rejected(self):
        path = '/' + 'Users' + '/someone/private/file'
        self.assertIn('machine-specific home path', package.inspect_contents('README.md', (path + '\n').encode()))

    def test_binary_rejected(self):
        self.assertIn('binary content', package.inspect_contents('README.md', b'x\x00y\n'))


if __name__ == '__main__':
    unittest.main()
