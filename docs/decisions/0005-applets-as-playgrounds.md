# 0005 — Applets are pure playgrounds; questions stay in class

- **Status:** accepted
- **Date:** 2026-10-05

## Context

Embedding questions in the applet (a "Predict" step before exploring, a list of experiments, external worksheets) was considered.

## Decision

Applets contain **no questions, quizzes or worksheets**. They are free-exploration playgrounds with an introduction, the interactive part, and a collapsible theory section.

Predictions and guided questions are handled by the teacher in class, with slides and live polls (AhaSlides), before or during the use of the applet.

## Reasons

- A mandatory question becomes friction when students reopen the applet at home to explore.
- In class, a live poll shows the distribution of the whole group's predictions, which is more effective than an individual question.
- The same applet serves different courses; the teacher adapts the questions to each audience without touching the code.
- Simpler applets are faster to build and maintain.

## Consequences

- The applet card may include "notes for the teacher" with suggested in-class questions. They never appear in the applet.
- Superseded proposal: embedded *Predict* / *Experiments* sections and per-course worksheets.
