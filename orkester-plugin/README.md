# orkester-plugin

A Cowork plugin for Orkester's business managers.

## What's included

- **Skill — propale-maker**: Helps the user through the different section of the content of a business proposal, with an emphasis on storytelling. Manages every other skill included in this plugin. Bases its answer on Orkester's past business proposals by accessing orkester-kb MCP connector.
- **Skill — propale-base-creator**: Selects and orders relevant sections from a catalogue based on a plot for a business proposal.
- **Skill — base-reviewer**: Reviews a selection of sections based on previous won business proposals, rates coherence, relevance, and storytelling. Meant to be executed in a clean context window.
- **Agent — skill-executor**: Subagent for executing skills with no biases, in a clean context window.

## Structure

```
orkester-plugin/
├── .claude-plugin/
│   └── plugin.json                       # Plugin manifest
├── skills/
│   ├── propale-maker/
│   │   ├── SKILL.md                      # Main skill to manage all the others
│   ├── propale-base-creator/
│   │   ├── SKILL.md                      # Propale plot creation skill
│   │   └── references/
│   │       └── catalogue-sections.md     # Collection of sections to use
│   ├── identity-creator/
│   │   ├── SKILL.md                      # Identity section writer
│   │   └── references/
│   │       └── bloc-B-identite.md        # Guidelines for redacting each section
│   └── base-reviewer/
│       └── SKILL.md                      # Plot reviewing skill
├── agents/
│   └── skill-executor.md                 # Fresh context agent for compartimented skill execution
└── README.md                             # This file
```
