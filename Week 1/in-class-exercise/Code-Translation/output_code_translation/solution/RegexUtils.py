import re
<<<<<<< Updated upstream

class RegexUtils:
    def match(self, pattern, text):
        return bool(re.search(pattern, text))

    def findall(self, pattern, text):
        return re.findall(pattern, text)

    def split(self, pattern, text):
        result = re.split(pattern, text)
        if not text:
            return result
        if result and result[0] != text:
            result.append("")
        return result

    def sub(self, pattern, replacement, text):
=======
from typing import List, Dict, Any


class RegexUtils:
    def match(self, pattern: str, text: str) -> bool:
        """Return True if the regex pattern is found anywhere in the text."""
        return re.search(pattern, text) is not None

    def findall(self, pattern: str, text: str) -> List[str]:
        """Return a list of all non‑overlapping matches of the pattern in the text."""
        return [m.group(0) for m in re.finditer(pattern, text)]

    def split(self, pattern: str, text: str) -> List[str]:
        """
        Split *text* by *pattern* similar to the C++ implementation.

        - If *text* is empty, return an empty list.
        - Otherwise, return the split parts; if the pattern matches at least once,
          an extra empty string is appended to the end (mirroring the original logic).
        """
        if text == "":
            return []

        parts = re.split(pattern, text)

        # The C++ version adds an empty string at the end when the first element
        # is not the whole original text (i.e., the pattern was found).
        if parts and parts[0] != text:
            parts.append("")
        return parts

    def sub(self, pattern: str, replacement: str, text: str) -> str:
        """Replace occurrences of *pattern* in *text* with *replacement*."""
>>>>>>> Stashed changes
        return re.sub(pattern, replacement, text)

    def generate_email_pattern(self):
        return r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    def generate_phone_number_pattern(self):
        return r"\b\d{3}-\d{3}-\d{4}\b"

    def generate_split_sentences_pattern(self):
        return r"[.!?][\s]{1,2}(?=[A-Z])"

<<<<<<< Updated upstream
    def split_sentences(self, text):
        pattern = self.generate_split_sentences_pattern()
        sentences = self.split(pattern, text)
        if sentences and not sentences[0]:
            sentences.pop(0)
        if sentences and not sentences[-1]:
=======
    def split_sentences(self, text: str) -> List[str]:
        """
        Split *text* into sentences using the generated split‑sentences pattern.
        Leading or trailing empty strings are removed to match the original C++ logic.
        """
        pattern = self.generate_split_sentences_pattern()
        sentences = self.split(pattern, text)

        # Remove leading empty string if present
        if sentences and sentences[0] == "":
            sentences.pop(0)

        # Remove trailing empty string if present
        if sentences and sentences[-1] == "":
>>>>>>> Stashed changes
            sentences.pop()

        return sentences

<<<<<<< Updated upstream
    def validate_phone_number(self, phone_number):
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

    def extract_email(self, text):
=======
    def validate_phone_number(self, phone_number: str) -> bool:
        """Validate that *phone_number* matches the phone‑number pattern."""
        pattern = self.generate_phone_number_pattern()
        return self.match(pattern, phone_number)

    def extract_email(self, text: str) -> List[str]:
        """Extract all email addresses found in *text*."""
>>>>>>> Stashed changes
        pattern = self.generate_email_pattern()
        return self.findall(pattern, text)
