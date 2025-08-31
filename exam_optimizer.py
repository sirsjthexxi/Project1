"""Utility functions to recommend exam time allocation based on strengths and weaknesses."""

from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class SectionPerformance:
    """Represents a student's proficiency in a section.

    Attributes:
        name: Name of the section or subject area.
        weight: Relative weight or marks of the section in the exam.
        proficiency: Value between 0 and 1 where 1 means very strong and 0 very weak.
    """

    name: str
    weight: float
    proficiency: float

    def __post_init__(self) -> None:
        if not 0 <= self.proficiency <= 1:
            raise ValueError("proficiency must be between 0 and 1")
        if self.weight < 0:
            raise ValueError("weight must be non-negative")


def allocate_time(sections: List[SectionPerformance], total_time: float) -> List[Tuple[str, float]]:
    """Compute the recommended time allocation for each section.

    The algorithm gives more time to sections with higher weight and lower proficiency.

    Args:
        sections: List of SectionPerformance entries.
        total_time: Total available time for the exam (in minutes).

    Returns:
        A list of tuples containing the section name and the recommended time to spend.
    """
    if total_time <= 0:
        raise ValueError("total_time must be positive")

    difficulty_scores = [s.weight * (1 - s.proficiency) for s in sections]
    total_difficulty = sum(difficulty_scores)

    if total_difficulty == 0:
        # If everything looks easy, split time evenly
        even_time = total_time / len(sections) if sections else 0
        return [(s.name, even_time) for s in sections]

    return [
        (s.name, total_time * score / total_difficulty)
        for s, score in zip(sections, difficulty_scores)
    ]


if __name__ == "__main__":
    demo_sections = [
        SectionPerformance("Math", weight=50, proficiency=0.8),
        SectionPerformance("Reading", weight=30, proficiency=0.5),
        SectionPerformance("Writing", weight=20, proficiency=0.2),
    ]
    for name, minutes in allocate_time(demo_sections, total_time=180):
        print(f"{name}: {minutes:.1f} minutes")
