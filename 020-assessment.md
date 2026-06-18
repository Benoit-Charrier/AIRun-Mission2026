
**Knowledge-check questions:**

1. _(W1)_ A team uses GitHub Copilot for code generation. Each developer configures it individually, prompts are not documented, and there are no metrics. What maturity level is this team at, and why?
    L1 — three signals lock them at L1 simultaneously: individual configuration (Reusability L1: siloed, no shared artifacts), no documentation (Reusability L1), and no metrics (Performance Tracking L1: anecdotal). Any one alone could still be L1; all three together means no path to L2 is even started.

2. _(W2)_ Name three examples of artifacts the AI Factory produces at different SDLC stages. Why is "a good prompt in a chat window" not an artifact in the AI Factory sense?
    User story, test case, shared prompt template — committed, versioned, and reusable. A chat prompt is not an artifact because it is not committed or versioned, so it cannot be reused by teammates.

3. _(W3)_ A project scores: AI Capabilities L2, Reusability L1, AI Champions L1, Performance Tracking L2, DAU L2. What is the overall maturity level? Which two dimensions are the critical blockers, and why?
    Average: 2+1+1+2+2 = 8 ÷ 5 = 1.6 = L1. Reusability and AI Champions are the critical blockers. Reusability L1 means prompts are siloed per person so the team cannot build on each other's work. AI Champions L1 means no mandate so adoption does not spread. Two L1s drag the overall level below 2.0 despite three dimensions at L2.

4. _(W3 / W4)_ Why is the team — not the individual — the primary unit of measurement in the AI Maturity Model? Give an example where individual productivity is high but team-level maturity stays at L1.
    Because AI gains do not spread if they stay with one person. Example: a developer uses AI to write tests but never commits the prompts — high individual output, zero reusability, zero spread. Team maturity stays at L1.

5. _(W5)_ Describe the "Chat as Delivery" anti-pattern. What does it look like in practice, and what does it block in the maturity model?
    Delivering a chat output instead of a committed artifact. In practice: the AI produces a result in a chat window, the person copies it into an email or document, and no artifact is committed to the repository. Blocks Reusability — the team stays at L1 because nothing is versioned or rerunnable by a teammate.

6. _(W6)_ Explain the difference between an agent and a sub-agent. Why is a tool call not the same as a step in an agentic workflow?
    An agent has a goal and can orchestrate sub-agents; a sub-agent is spawned by an orchestrator to handle a bounded sub-task. A tool call is pure execution — deterministic, no memory, no decision. An agentic workflow step reasons on the result, decides what to do next, and can call different tools depending on what it finds — it holds state across steps. The extra ingredient is decision-making based on previous results.

7. _(W7)_ A developer spends three hours in an interactive Claude Code session iterating on a refactoring task. Their `CLAUDE.md` is committed, but cache hit rate is below 20%. Name the anti-pattern at work, the maturity transition it blocks, and one specific change that would raise the cache hit rate.
    Anti-pattern: run spend over spec spend — three hours of interactive iteration burns tokens on ephemeral conversation context instead of investing once in stable spec that gets cached. Blocks L2→L3 because agentic workflows require codified, cacheable spec to run efficiently at scale. Fix: move task description, constraints, and code context into CLAUDE.md so the stable portion dominates the context and cache hit rate rises.

**Self-reflection questions:**

1. _(W3)_ Score your current project on the Reusability dimension. What specifically is stored under source control from your AI work? If nothing — what would be the first concrete step?
    L2-pending — prompt-template-domain-research.md committed to output repo. Reusability becomes solid L2 once Dmytro runs the template independently (peer review in progress).

2. _(W4 / W5)_ Does your project have an AI Champion? If yes — what does that person do that others don't? If no — who could take that role, and what is preventing it?
    No AI Champion on the Meridian reference case — no mandate across three SI partners. No active project context currently (FDE Program has ended).

3. _(W1 / W5)_ Think of the last time you used AI for a work task. Is the result reusable by a teammate without your explanation? If not — what would you do differently?
    Yes — the domain research output (domain-research.md) is reusable. The committed prompt template means a teammate can reproduce it without asking for help.

4. _(W7)_ Pick one workflow on your current project that uses AI. Estimate where the tokens are spent today — spec creation or interactive runs. What would shift that distribution toward more spec spend?
    The domain research workflow was mostly interactive runs. Committing the D0A prompt template (Kata 2) shifted it toward spec spend — the template is now the stable spec that drives consistent outputs each time it is run.
    
