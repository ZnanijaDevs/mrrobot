import re
from dataclasses import dataclass


@dataclass
class Question:
    created: str
    content: str
    answers_count: int
    subject: str | None = None

    @staticmethod
    def _filter_content(content: str) -> str:
        """Filter a content of question/answer"""
        filtered_content = content

        replacements = [
            (r"<br\s\/>", "\n"),
            (r"<\/?\w+\s?\/?>", ""),
            (r"\n{2,}|\n\s*\n", "\n"),
            (r"^(\s|\n)|(\s?\n)$", "")
        ]

        for regex, new in replacements:
            filtered_content = re.sub(regex, new, filtered_content)

        filtered_content = filtered_content.strip()

        return filtered_content

    @staticmethod
    def from_dict(it: dict):
        return Question(**it)

    @property
    def filtered_content(self):
        if self.content:
            return self._filter_content(self.content)

    @property
    def short_content(self):
        if self.content:
            return self.filtered_content[:300] if len(self.filtered_content) > 300 else self.filtered_content


class GQLQuestion(Question):
    @staticmethod
    def from_dict(it: dict):
        return Question(
            created=it["created"],
            content=it["content"],
            subject=it["subject"]["name"] if it.get("subject") else None,
            answers_count=len(it["answers"]["nodes"])
        )
