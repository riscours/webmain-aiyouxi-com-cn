from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

EXAMPLE_URL = "https://webmain-aiyouxi.com.cn"
EXAMPLE_KEYWORD = "爱游戏"


@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    note: str
    source_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "keyword": self.keyword,
            "note": self.note,
            "source_url": self.source_url,
            "tags": self.tags[:],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


@dataclass
class KeywordNoteCollection:
    """A collection of keyword notes with search and formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_all_notes(self) -> str:
        """Return a multi-line formatted string of all notes."""
        if not self.notes:
            return "No notes available."

        lines = []
        for i, note in enumerate(self.notes, start=1):
            lines.append(f"--- Note {i} ---")
            lines.append(f"Keyword: {note.keyword}")
            lines.append(f"Note: {note.note}")
            if note.source_url:
                lines.append(f"Source: {note.source_url}")
            if note.tags:
                lines.append(f"Tags: {', '.join(note.tags)}")
            lines.append(f"Created: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            if note.updated_at:
                lines.append(f"Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M')}")
            lines.append("")
        return "\n".join(lines)

    def format_summary(self) -> str:
        """Return a compact summary of all notes."""
        summary_parts = [f"Total notes: {len(self.notes)}"]
        all_tags = set()
        for n in self.notes:
            all_tags.update(n.tags)
        if all_tags:
            summary_parts.append(f"Tags used: {', '.join(sorted(all_tags))}")
        if self.notes:
            summary_parts.append(f"Keywords: {', '.join(n.keyword for n in self.notes)}")
        return " | ".join(summary_parts)


def create_sample_collection() -> KeywordNoteCollection:
    """Create a sample keyword note collection with example data."""
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword="爱游戏",
        note="用户对游戏平台的核心关注点，包括用户体验和内容质量。",
        source_url="https://webmain-aiyouxi.com.cn",
        tags=["游戏", "用户研究"],
    )
    collection.add_note(note1)

    note2 = KeywordNote(
        keyword="游戏社区",
        note="社区互动和用户生成内容是提升粘性的关键。",
        source_url="https://webmain-aiyouxi.com.cn/community",
        tags=["社区", "用户研究"],
    )
    collection.add_note(note2)

    note3 = KeywordNote(
        keyword="爱游戏",
        note="竞品分析：爱游戏平台在内容推荐方面的做法。",
        tags=["竞品分析", "内容"],
    )
    collection.add_note(note3)

    return collection


def main():
    """Demonstrate usage of keyword notes module."""
    collection = create_sample_collection()

    print("=== All Notes ===")
    print(collection.format_all_notes())

    print("=== Summary ===")
    print(collection.format_summary())

    print("\n=== Search by keyword '爱游戏' ===")
    results = collection.find_by_keyword("爱游戏")
    for note in results:
        print(f"  - {note.keyword}: {note.note}")

    print("\n=== Search by tag '用户研究' ===")
    results = collection.find_by_tag("用户研究")
    for note in results:
        print(f"  - {note.keyword}: {note.note}")


if __name__ == "__main__":
    main()