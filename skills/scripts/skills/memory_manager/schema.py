"""Pydantic schemas for memory validation."""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class BugFixed(BaseModel):
    """Schema for a bug that was fixed."""
    description: str = Field(description="Brief description of the bug")
    root_cause: str = Field(description="Why the bug occurred")
    solution: str = Field(description="What fixed it")
    prevention: Optional[str] = Field(default=None, description="How to avoid future recurrence")


class ProblemSolution(BaseModel):
    """Schema for problem-solution pair."""
    problem: str = Field(description="What didn't work and why")
    solution: str = Field(description="What worked and why")


class Decision(BaseModel):
    """Schema for notable decision."""
    description: str = Field(description="Brief description of the decision")
    rationale: str = Field(description="Why this choice was made")
    trade_offs: Optional[str] = Field(default=None, description="What was sacrificed")
    alternatives_rejected: Optional[List[str]] = Field(default=None, description="What was considered but not chosen")


class SessionContext(BaseModel):
    """Schema for session context."""
    working_directory: str = Field(description="Primary working directory")
    primary_goal: str = Field(description="Main objective of the session")
    duration: Optional[str] = Field(default=None, description="Approximate session duration")


class SessionMemory(BaseModel):
    """Complete schema for session memory."""
    session_number: int = Field(description="Sequential session number for the day")
    date: str = Field(description="Session date in YYYY-MM-DD format")
    time: str = Field(description="Session start time in HH:MM format")
    context: SessionContext
    goals_accomplished: List[str] = Field(description="Specific outcomes achieved")
    bugs_fixed: List[BugFixed] = Field(default_factory=list, description="Bugs fixed during session")
    patterns_discovered: List[str] = Field(default_factory=list, description="Reusable architectural or debugging insights")
    problem_solutions: List[ProblemSolution] = Field(default_factory=list, description="What didn't work vs what did")
    future_avoidance: List[str] = Field(default_factory=list, description="Prevention strategies for mistakes")
    notable_decisions: List[Decision] = Field(default_factory=list, description="Decisions with rationale")
    invisible_knowledge: List[str] = Field(default_factory=list, description="Rationale not evident from code")
    references: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Related sessions, files modified, external links"
    )


class MasterMemoryEntry(BaseModel):
    """Schema for MASTER-MEMORY.md entry."""
    date: str = Field(description="Session date in YYYY-MM-DD format")
    session_number: int = Field(description="Sequential session number for the day")
    summary: str = Field(description="1-2 sentence summary of session")
    key_topics: List[str] = Field(description="Main topics covered")


class QuickMemory(BaseModel):
    """Schema for memory.md quick reference."""
    recent_sessions: List[Dict[str, str]] = Field(
        description="List of recent session summaries with date, session_number, summary"
    )
    active_patterns: List[str] = Field(
        default_factory=list,
        description="Currently relevant patterns"
    )
    current_context: str = Field(description="Brief current state of project")
