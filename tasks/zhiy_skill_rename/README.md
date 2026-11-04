# local/zhiy_skill_rename

Tests whether an agent's harness supports skills. The instruction asks for a
rename under a "naming convention" without saying what it is or mentioning
skills. The new name comes from a script in the `rename-python-variable` skill,
so the agent has to find the skills in `/skills`, choose that one over the
similar `rename-sql-column` skill, open it, and run its script.

An agent with no skill support should earn 0. If one earns 1, it probably
searched the disk and found `/skills`, so check its trajectory.

This task can't tell whether skill bodies are loaded only when needed. A harness
that puts every skill in the prompt up front could still pass.
