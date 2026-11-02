# local/zhiy_clue_chain

Tests whether an agent can sustain a long sequence of dependent steps. Each of
the 60 clues is encrypted with a key derived from the previous answer, so later
clues can't be read ahead of time, and their varied wording is meant to need a
model decision each time.

An agent with a step cap below about 60 should run out of steps before finishing.
