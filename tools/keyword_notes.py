from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

SAMPLE_URL = "https://zhm-hth.com.cn"
SAMPLE_KEYWORD = "华体会"


@dataclass
class KeywordNote:
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def formatted_brief(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.keyword}] ({self.url}) 标签: {tag_str}"

    def formatted_detail(self) -> str:
        lines = [
            f"关键词: {self.keyword}",
            f"来源URL: {self.url}",
            f"备注: {self.note or '无'}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
            f"创建时间: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        return "\n".join(lines)


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword in n.keyword]

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def formatted_all(self, detail: bool = False) -> str:
        if not self.notes:
            return "暂无笔记。"
        parts = [f"共 {len(self.notes)} 条笔记："]
        for i, note in enumerate(self.notes, 1):
            if detail:
                parts.append(f"--- 笔记 {i} ---\n{note.formatted_detail()}")
            else:
                parts.append(f"{i}. {note.formatted_brief()}")
        return "\n".join(parts)

    def export_to_text(self, filepath: str) -> None:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(self.formatted_all(detail=True))


def create_sample_notes() -> KeywordNoteCollection:
    collection = KeywordNoteCollection()
    collection.add(KeywordNote(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        note="这是一个示例关键词笔记，用于演示 dataclass 用法。",
        tags=["示例", "测试"],
    ))
    collection.add(KeywordNote(
        keyword="Python",
        url="https://python.org",
        note="Python 编程语言官方网站。",
        tags=["技术", "编程"],
    ))
    collection.add(KeywordNote(
        keyword="数据类",
        url="https://docs.python.org/zh-cn/3/library/dataclasses.html",
        note="Python dataclass 官方文档。",
        tags=["技术", "Python", "文档"],
    ))
    return collection


def main() -> None:
    notes = create_sample_notes()
    print("简要列表：")
    print(notes.formatted_all(detail=False))
    print("\n详细列表：")
    print(notes.formatted_all(detail=True))


if __name__ == "__main__":
    main()