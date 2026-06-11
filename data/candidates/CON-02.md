INTERNAL MEMO
To: Operations Steering Committee
Re: AI-assisted claims intake summarization — design, rollout, and 90-day results

Background. Our claims intake team of 14 adjusters spent an average of 35 minutes per file assembling first-notice-of-loss summaries from inconsistent broker documents. I proposed and led the workflow described below.

1. Problem selection. I shortlisted three candidate processes with the operations lead and chose intake summarization because it was high-volume, low-ambiguity, and carried no settlement authority. Processes touching coverage decisions were excluded from scope at the outset.

2. Workflow design. The workflow runs in four steps: document ingestion, AI-drafted summary, adjuster review and correction, and supervisor sign-off for files above $50,000. The AI drafts; the adjuster owns the file. We defined at the outset that the system would never determine coverage or reserve amounts. I configured the pipeline in Power Automate against an internal prompt library that I maintain.

3. Governance. I brought the design to our risk committee before any build began, documented the data flows for privacy review, and agreed an audit sample of 5% of AI-drafted summaries reviewed monthly by quality assurance.

4. Change management. Two adjusters piloted the workflow for three weeks; their corrections reshaped the prompt twice before wider rollout. We trained the full team in two sessions, and adoption reached 12 of 14 adjusters by week six.

5. Results. Average intake time fell from 35 minutes to 14 minutes per file. The quality audit found 2 material errors across 240 sampled summaries, both caught at adjuster review before any downstream impact.

6. What I would do differently. I assumed the broker document formats were consistent; they were not. We added a format-normalization step in week two, which delayed the pilot by eight days but removed the largest source of drafting errors.

Recommendation. Extend the pattern to subrogation intake next quarter, with the same human-ownership boundary and audit sampling.
