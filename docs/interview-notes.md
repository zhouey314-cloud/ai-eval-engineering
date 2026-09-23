# Interview notes

1. **Why?** To make ai-eval-engineering an inspectable, reusable portfolio artifact.
2. **Hardest problem?** Distinguishing deterministic checks from model quality.
3. **Why this architecture?** Keep core workflow logic separate from UI and external providers.
4. **Where is AI?** Read the README for the precise AI or prompt boundary; do not infer model quality from tests.
5. **What stays human?** Domain truth, final review and external publishing decisions.
6. **How verified?** Run the documented tests and inspect their actual assertions.
7. **Failure learned?** Synthetic ground truth is not expert verified.
8. **Redo?** Add stronger, reviewed regression cases before claiming broader reliability.
9. **Production scale?** Add authentication, observability, durable storage and verified integrations as relevant.
10. **My contribution?** The public repository's code, documentation and tests; avoid claiming third-party or company work as original.
