Context Preparation Flow

  1. Workspace Location

  The workspace is determined in pkg/agent/instance.go:

  • Default: ~/.picoclaw/workspace/ (or configured via AgentConfig.Workspace)
  • Agent-specific: ~/.picoclaw/workspace-{agentID}/ for non-default agents

  2. Bootstrap Files Loaded (pkg/agent/context.go:336-353)

  These files from the workspace directory are loaded into the system prompt:

   File               Purpose
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   AGENTS.md          General agent instructions and guidelines
   SOUL.md            Personality, values, and behavior traits
   USER.md            User preferences and personal information
   IDENTITY.md        Agent identity (name, version, capabilities)
   memory/MEMORY.md   Long-term memory storage

  3. Skills Loading (pkg/skills/loader.go:76-124)

  Skills are discovered from three sources (in priority order):

  1. Workspace skills: {workspace}/skills/{skill-name}/SKILL.md
  2. Global skills: ~/.picoclaw/skills/{skill-name}/SKILL.md
  3. Builtin skills: {cwd}/skills/{skill-name}/SKILL.md

  Only the skill summary (name, description, path, source) is loaded into context - not the full skill conte
  nt.

  4. System Prompt Assembly (pkg/agent/context.go:86-116)

  The final system prompt is built in this order:

  1. Core Identity (hardcoded base + workspace path)
  2. Bootstrap Files (AGENTS.md, SOUL.md, USER.md, IDENTITY.md)
  3. Skills Summary (list of available skills)
  4. Memory Context (from MEMORY.md)

  Separated by --- dividers.

  5. Dynamic Context (pkg/agent/context.go:363-375)

  Per-request dynamic info is added (not cached):

  • Current time
  • Runtime info (OS, architecture, Go version)
  • Current session (channel, chat ID)

  6. Caching (pkg/agent/context.go:119-158)

  The static parts of the system prompt are cached and auto-invalidated when:

  • Any bootstrap file is modified, created, or deleted
  • Skills directory changes
  • Memory file changes

  Cache uses mtime checks for efficient invalidation.

  ──────────────────────────────────────────────────────────────────────────────────────────────────────────
  Summary: What Gets Loaded Into Each Session

   Component              Source                                     Cached?
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Core identity          Hardcoded + workspace path                 ✅ Yes
   AGENTS.md              workspace/AGENTS.md                        ✅ Yes
   SOUL.md                workspace/SOUL.md                          ✅ Yes
   USER.md                workspace/USER.md                          ✅ Yes
   IDENTITY.md            workspace/IDENTITY.md                      ✅ Yes
   Skills summary         workspace/skills/*, ~/.picoclaw/skills/*   ✅ Yes
   Memory                 workspace/memory/MEMORY.md                 ✅ Yes
   Current time           Generated                                  ❌ No
   Session info           Generated                                  ❌ No
   Conversation history   Session storage                            ❌ No

  The default workspace template is embedded in the binary at workspace/ and copied on first run.
