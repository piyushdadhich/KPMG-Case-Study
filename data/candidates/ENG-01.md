# triage-copilot

Agentic ticket triage for an internal IT service desk. Built solo over six weeks; now running in our team's staging environment with the dispatch team trialling it daily.

## What it does

- Ingests new ServiceNow tickets via webhook
- A classifier agent assigns category and urgency
- A routing agent proposes an assignment group; a human dispatcher approves or overrides every routing proposal before it is applied
- Classifier confidence below 0.7 falls back to the legacy keyword router

## Why human approval is mandatory

Mis-routed P1 tickets breach SLA. The agent proposes; the dispatcher disposes. Autonomy is limited to drafting, never to acting on production queues.

## Eval harness

- 400 hand-labelled historical tickets live in /evals
- A nightly regression run executes in CI; deploys block if category F1 drops below 0.86
- Prompt changes require a passing eval run attached to the PR

## Stack

Python 3.12, FastAPI, LangGraph, Postgres, GitHub Actions.

## Install

```
pip install -r requirements.txt
make evals && make run
```

## Known limitations

- No cost cap on the classifier loop yet (tracked in issue #41)
- The eval set under-represents hardware tickets
- Staging only; production rollout pending change-board review
