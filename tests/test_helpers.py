"""Offline checks of input boundaries, alignment and sharing safeguards."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


qwen = load('qwen', 'skills/explain-video/scripts/qwen_narration.py')
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
        cues = qwen.load_cues(ROOT / 'skills/explain-video/examples/narration.json', limit=1)
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

    def test_bookmarks_resolve_to_spoken_phrase_and_survive_sentence_insertion(self):
        phrase = {'lost_reply': 'the reply is lost'}
        for prefix in ['', 'The server commits. ']:
            text = prefix + 'The request succeeds. The reply is lost.'
            words = [{'word': w, 'start': i * .5, 'end': i * .5 + .4}
                     for i, w in enumerate(text.split())]
            marks = qwen.resolve_landmarks(text, words, 10, phrase)
            offset = len(prefix.split()) * .5
            self.assertEqual(marks['lost_reply'], {'start': offset + 1.5, 'end': offset + 3.4})

    def test_missing_ambiguous_and_empty_bookmarks_fail_before_synthesis(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'script.json'
            for bookmarks in [{'retry': 'missing phrase'}, {'retry': 'retry'}, {'retry': ''}, []]:
                path.write_text(json.dumps([{'id': 'retry', 'text': 'Retry now. Retry later.',
                                             'bookmarks': bookmarks}]))
                with self.assertRaisesRegex(ValueError, 'Bookmark'):
                    qwen.load_cues(path)

    def test_invalid_word_timestamps_rejected(self):
        for start, end in [(-1, .2), (1, .5), (0, float('nan')), (0, 9)]:
            with self.assertRaisesRegex(ValueError, 'ASR word timing'):
                qwen.resolve_landmarks('Hello.', [{'word': 'Hello', 'start': start, 'end': end}],
                                       2, {'hello': 'Hello'})

    def test_reordering_or_renaming_cues_preserves_speech_cache(self):
        settings = {'seed': 731, 'speaker': 'Ryan', 'model_identity': 'first'}
        original = [{'id': 'first', 'text': 'Hello.'}, {'id': 'second', 'text': 'Goodbye.'}]
        revised = [{'id': 'new', 'text': 'Welcome.'}, {'id': 'renamed', 'text': 'Goodbye.'}, original[0]]
        keys = lambda cues: {c['text']: qwen.cache_key(qwen.speech_identity(c['text'], settings)) for c in cues}
        before, after = keys(original), keys(revised)
        self.assertTrue(all(before[text] == after[text] for text in before))
        identity = qwen.speech_identity('Hello.', settings)
        self.assertNotEqual(identity['cue_seed'], qwen.speech_identity('Goodbye.', settings)['cue_seed'])

    def test_text_voice_or_weights_invalidate_speech(self):
        settings = {'seed': 731, 'speaker': 'Ryan', 'model_identity': 'first'}
        before = qwen.cache_key(qwen.speech_identity('Hello.', settings))
        for text, changed in [('Hello!', settings), ('Hello.', {**settings, 'speaker': 'Other'}),
                              ('Hello.', {**settings, 'model_identity': 'other'})]:
            self.assertNotEqual(before, qwen.cache_key(qwen.speech_identity(text, changed)))

    def test_asr_changes_invalidate_alignment_and_preserve_speech(self):
        speech = qwen.cache_key(qwen.speech_identity('Hello.', {'seed': 731, 'speaker': 'Ryan'}))
        settings = {'asr_prompt': 'English.', 'asr_identity': 'first', 'alignment_version': 5}
        before = qwen.cache_key(qwen.alignment_identity(speech, 'audio', settings))
        for changed in [{**settings, 'asr_prompt': 'Technical English.'},
                        {**settings, 'asr_identity': 'other'}, {**settings, 'alignment_version': 6}]:
            identity = qwen.alignment_identity(speech, 'audio', changed)
            self.assertEqual(identity['speech_key'], speech)
            self.assertNotEqual(before, qwen.cache_key(identity))
        self.assertNotEqual(before, qwen.cache_key(qwen.alignment_identity(speech, 'changed audio', settings)))


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


class PackageLayoutTests(unittest.TestCase):
    def test_each_skill_has_resolvable_links_when_installed_alone(self):
        for name in package.PACKAGES:
            with self.subTest(skill=name), tempfile.TemporaryDirectory() as temp:
                dest = Path(temp) / name
                shutil.copytree(ROOT / 'skills' / name, dest)
                for path in dest.rglob('*.md'):
                    self.assertEqual(package.markdown_link_failures(path, path.read_text(), dest), [],
                                     str(path.relative_to(dest)))
                for relative in package.PACKAGES[name]:
                    self.assertTrue((dest / relative).is_file(), relative)

    def test_link_to_a_sibling_package_is_rejected_even_if_it_exists(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / 'one'
            skill.mkdir()
            sibling = root / 'two.md'
            sibling.write_text('Sibling.\n')
            failures = package.markdown_link_failures(skill / 'SKILL.md', '[other](../two.md)', skill)
            self.assertEqual(failures, ['local reference escapes distribution boundary'])

    def test_bundled_player_stays_identical_between_packages(self):
        paths = [ROOT / 'skills' / name / 'assets/film-player.js' for name in package.PACKAGES]
        self.assertEqual(paths[0].read_bytes(), paths[1].read_bytes())


if __name__ == '__main__':
    unittest.main()
