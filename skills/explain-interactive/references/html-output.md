# Offline page and interaction contract

Read before building the standalone HTML artifact. Keep subject-specific state and explanations in the page; the learner should not need the chat to reconstruct what is happening.

## Document and layout

Create one UTF-8 document with doctype, descriptive title, language and viewport metadata. Inline essential styles, scripts, source fixtures and assets so it works from `file://`. Avoid a development server, adjacent JSON fetches, CDN dependencies and host-specific widget runtimes. Include clickable source/version links. Disclose any genuinely unavoidable external dependency.

Use readable typography, visible keyboard focus and sufficient contrast. Preserve warm paper, dark ink and restrained accents unless another direction was chosen. The optional [lesson.css](../assets/lesson.css) is a starting point to inline, not a fixed layout.

A self-paced explanation can use a purposeful vertical sequence, while a timed film player should keep stage, captions and controls together within the viewport. Keep navigation connected to the reasoning rather than accumulating every supplementary resource. Details and source inspection can be separate views. A modal must support Close and Escape, preserve the learning state and restore focus.

Use semantic lists and `<pre>` for code, with `white-space: pre` or `pre-wrap`. Recompose narrow layouts instead of shrinking dense text. Do not rely on hover, color or motion alone to communicate meaning.

## State and controls

Prefer HTML/SVG, CSS and explicit JavaScript state. Compute state transitions from the fixture, then render them; cancel obsolete animations during navigation. Keep entity names and values consistent across frames and explain when an operation changes their meaning. Place a condition or cause beside the change it drives.

Choose previous/next/replay for manual traces, selection controls for contrasting cases, or inputs for genuine experiments. Derive displayed results from changed inputs. Preserve the meaning of empty, failed or boundary cases. The [synthetic retry trace](../assets/retry-trace.html) demonstrates a serialized worker and lost reply. Its pseudocode does not model concurrent workers, crash recovery or durable idempotency and is not source material for unrelated topics.

For timed playback, keep one master clock and reconstruct every view from time. Provide pause, seek, replay, keyboard handling and speed options including 0.8× and 0.9×. Never loop continuously or pause for questions unless the learner chose that mode. Read [player-runtime.md](player-runtime.md) when using the included player and viewport shell. A framework or GSAP is optional when its timing or state support warrants it.

For reduced motion, expose the same states and meaning without sweeping transitions. Optional predictions can hide a revealing result until the learner chooses to reveal it, without compulsory entry or keyword grading. A revealed answer does not establish an independent prediction.

If narration was requested, preserve the selected voice and provider using available tools, embed essential audio, and verify pause/seek/speed/end synchronization. Keep captions and explanation usable with sound muted. Do not put a model call behind every animation step or send the learner's state anywhere without a requested purpose.

## Verify the actual file

Open the saved offline file, not only the development version. Exercise meaningful branches, previous/next/replay, rapid navigation, keyboard access and reduced motion. For timed playback, also test arbitrary seeks, speed changes and end/replay. Test changed inputs, audio and detail views when present. Check narrow and short windows, actual text geometry, runtime errors and essential network requests.

Return its absolute file link and open it in Google Chrome unless another browser was chosen. On macOS an argument-safe call is `subprocess.run(['open', '-a', 'Google Chrome', str(html_path)], check=True)`. Respect local work-profile instructions without baking account names into the shared skill. Report a launch failure while retaining the file. Browser checks do not establish source-system execution or learning effectiveness.
