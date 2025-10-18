import re
from pathlib import Path
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import docx
import unicodedata
import csv
from pypdf import PdfReader
from collections import defaultdict
from string import punctuation


def extract_ssa_text(filepath):
    """
    Removes timestamps and formatting from SSA-formatted subtitle files.

    Args:
        filepath (str): The path to a file containing some text.

    Returns:
        str: The text from the file, with timestamps/formatting removed.
    """
    filepath = Path(filepath)

    with open(filepath, encoding="utf-8-sig") as f:
        text = f.read()

    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.split(",", 9)
            if len(parts) == 10:
                dialogue_text = parts[-1]
                dialogue_text = re.sub(r"\{.*?\}", "", dialogue_text)
                dialogue_text = re.sub(r'\\[Nn]', ' ', dialogue_text)

                cleaned_lines.append(dialogue_text)

    return unicodedata.normalize("NFC", " ".join(cleaned_lines))

def extract_text_from_file(filepath):
    """
    Removes timestamps and formatting from SRT subtitle files.

    Args:
        filepath (str): The path to a file containing some text.

    Returns:
        str: The text from the file, with timestamps/formatting removed.
    """
    valid_formats = ['.srt', '.txt', '.md', '.docx', '.pdf', '.epub']

    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Error: The file '{filepath}' was not found.")

    if not any(filepath.suffix == ext for ext in valid_formats):
        raise IOError(
            f"Error: Could not read the file contents of '{filepath.name}'."
            " File format is invalid.")

    try:
        timestamp_pattern = (
            r'\d+\s+'
            r'\d{2}:\d{2}:\d{2},\d{3} --> '
            r'\d{2}:\d{2}:\d{2},\d{3}\s*'
        )
        tag_pattern = r'<.*?>'
        combined_pattern = rf"{timestamp_pattern}|{tag_pattern}"

        if filepath.suffix == '.docx':
            doc = docx.Document(filepath)
            text = '\n'.join([p.text for p in doc.paragraphs])

        elif filepath.suffix == '.pdf':
            pdf_reader = PdfReader(filepath)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

        elif filepath.suffix == '.epub':
            book = epub.read_epub(str(filepath))
            text = ""
            for item in book.get_items():
                if item.get_type() == ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text += soup.get_text().strip()

        else:
            with open(filepath, encoding="utf-8-sig") as f:
                lines = f.readlines()

            first_line = next(
                (
                    line.strip() for line in lines if line.strip()
                ),
                ""
            )

            if first_line.startswith("[Script Info]"):
                text = extract_ssa_text(filepath)
            else:
                text = "".join(lines)

        cleaned_text = re.sub(combined_pattern, "", text)
        cleaned_text = re.sub(
            r'[\u200B\u200C\u200D\u2060\uFEFF]', '', cleaned_text
            )
        cleaned_text = re.sub(r'\\an8}', '', cleaned_text)
        cleaned_text = re.sub(r'\d\.\w+(?:\.\w+)?', '', cleaned_text)
        cleaned_text = re.sub(r'(?<=\w)—(?=\w)', ' ', cleaned_text)
        cleaned_text = unicodedata.normalize("NFC", cleaned_text)

        return cleaned_text

    except RuntimeError:
        raise RuntimeError(f"Error: Could not read the file '{filepath}'")

def generate_word_list(text):
    """
    Generates a list of words and word frequencies in a given text.

    Args:
        text (str): Text containing the words to be counted.

    Returns:
        dict: A dictionary containing words and word counts.
    """
    word_freq = defaultdict(int)
    punc_chars = punctuation + '¿¡♪«»—©‘’–‚”“„•'
    if text:
        words = text.lower().split()
        for word in words:
            word = re.sub(rf'^[{punc_chars}]*|[{punc_chars}]*$', '', word)
            if word and not word.isnumeric():
                word_freq[word] += 1
    return word_freq

def convert_word_list_to_csv(words, filepath):
    """
    Creates a CSV file containing words and word frequencies from a given text.

    Args:
        words (dict): A dictionary containing words and word frequencies.
        filepath (str): The intended filepath of the CSV file.

    Returns:
        None
    """
    sorted_words = sorted(words.items())

    with open(filepath, mode="w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        for word, count in sorted_words:
            if word:
                writer.writerow([word, count])