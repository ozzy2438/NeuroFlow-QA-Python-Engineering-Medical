# NeuroFlow QA Validation Notes

## Validation idea

This project uses deterministic, explainable rules rather than a black-box model. That is intentional. In regulated or clinical-adjacent software, the first version of a quality system should be easy to inspect.

## QC rules used

- Flag if T1 SNR is too low.
- Flag if fMRI temporal SNR is too low.
- Flag if frame-to-frame fMRI variation is too high.
- Flag if synthetic head motion is above threshold.
- Flag if synthetic brain-like volume is outside expected range.

## Why rule-based first?

A rule-based system is easier to explain during interviews. It shows that the candidate understands reliability, validation, traceability, and failure reasons before jumping into machine learning.

## Current validation result

- Subject count: 100
- Passed: 62
- Flagged: 38

## Next improvement

The next version can add unit tests, CLI execution, Docker packaging, and comparison against manual reviewer labels.
