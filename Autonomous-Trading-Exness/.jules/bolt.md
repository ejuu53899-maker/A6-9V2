## 2026-03-03 - [System Initialization]
**Learning:** A performance agent is only as good as its data integrity. Cleanup of "Jules' memory" is a prerequisite for optimization to prevent "hallucinated bottlenecks."
**Action:** Audit all existing .jules/ documentation for stale logic before implementing code changes.

### Memory Review: Jules (Verification & Cleanup)
I have analyzed the concept of "Jules' memory." Here is the documentation update:

✅ TRUE (Keep & Document)
- Contextual Persistence: Jules must maintain state across sessions to avoid redundant re-calculations.
- Instruction Supremacy: Performance boundaries (no package.json edits, no breaking changes) are the "hard truths" of the system.
- Measurement First: Any "memory" regarding performance gains must be backed by a benchmark, not an assumption.

❌ FALSE (Clean up & Purge)
- Stale References: Any documentation suggesting npm when the project uses pnpm is a performance drag (cache misses).
- Deprecated Patterns: Removing references to useEffect for data fetching where a cache-first library (like TanStack Query) is already present.
- Redundant Logs: Purging verbose logging that slows down the production runtime.
