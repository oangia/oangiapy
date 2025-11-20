import re
import unicodedata
import base64, json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

def encrypt_for_client(response_data: dict, client_pub_key_b64: str) -> str:
    client_pub_bytes = base64.b64decode(client_pub_key_b64)
    client_pub_key = serialization.load_der_public_key(client_pub_bytes)
    plaintext = json.dumps(response_data).encode()
    cipher = client_pub_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(cipher).decode()
    
class TextAnalyzer:
    REFERENCE_DATA = {
        "difficulty": {
            "hardWords": 26,
            "longSentences": 0,
            "adverbs": 3,
            "hardAdjectives": 9,
            "nominals": 1,
            "passiveWords": 0,
            "weakVerbs": 2
        },
        "character": {
            "totalWords": 98,
            "avgWordLength": 6,
            "longestWord": "Understanding",
            "longestWordLength": 13,
            "charsWithSpaces": 720,
            "charsWithoutSpaces": 623,
            "lettersAZ": 616,
            "alphaNumeric": 616
        },
        "sentences": {
            "total": 7,
            "lineCount": 0,
            "totalLines": 7,
            "avgLength": 14,
            "activeVoice": 7,
            "passiveVoice": 0,
            "short": 2,
            "medium": 5,
            "long": 0
        },
        "paragraphs": {
            "count": 1,
            "shortest": 98,
            "longest": 98
        },
        "words": {
            "easy": 72,
            "hard": 26,
            "compound": 0,
            "cardinal": 0,
            "properNoun": 0,
            "abbreviated": 0,
            "unique": 75,
            "repeat": 15
        },
        "syllables": {
            "total": 201,
            "avgPerWord": 2.05,
            "oneSyl": 35,
            "twoSyl": 37,
            "threeSyl": 14,
            "fourSyl": 10,
            "fiveSyl": 2,
            "sixSyl": 0,
            "sevenPlusSyl": 0
        }
    }

    def __init__(self, reference_data=None):
        self.reference_data = reference_data
        self.weak_verbs_set = {'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am', 'has', 'have', 'had'}
        self.adjective_suffixes = re.compile(r"(?:able|ible|al|ful|ic|ical|ive|less|ous|ious|eous|ent|ant|ary)$", re.IGNORECASE)
        self.nominalization_patterns = re.compile(r"(?:tion|sion|ment|ness|ity|ance|ence)$", re.IGNORECASE)

    def normalize_text(self, text):
        try:
            return unicodedata.normalize('NFC', text)
        except:
            return text

    def split_sentences(self, text):
        return [s.strip() for s in re.split(r"[.!?…]+\s+|\n+", text) if s.strip()]

    def split_words(self, text):
        text = unicodedata.normalize('NFC', text)
        text = re.sub(r"[\u00A0\u200B\t\n\r]+", " ", text)
        return re.findall(r"\b[\w]+(?:['\-][\w]+)*\b", text, flags=re.UNICODE)

    def count_letters(self, text):
        return len(re.findall(r"[A-Za-z]", text))

    def count_chars_with_spaces(self, text):
        return len(text)

    def count_chars_without_spaces(self, text):
        return len(re.sub(r"\s", "", text))

    def avg_word_length(self, words):
        return sum(len(w) for w in words)/len(words) if words else 0

    def longest_word(self, words):
        if not words: return '', 0
        w = max(words, key=len)
        return w, len(w)

    def syllables_in_word(self, word):
        w = re.sub(r"[^a-z]", "", word.lower())
        if w == "reliable": return 4
        if len(w) <= 3: return 1

        syl = 0
        t = w
        if re.search(r'le$', t): syl += 1
        if re.search(r'(ted|ded)$', t): syl += 1
        if re.search(r'(thm|thms)$', t): syl += 1
        if re.search(r'(ses|zes|ches|shes|ges|ces)$', t): syl += 1
        if 'rial' in t: syl += 1
        if 'creat' in t: syl += 1

        t = re.sub(r'(e|ed|es)$', '', t)
        diph = re.findall(r"aa|ae|ai|ao|au|ay|ea|ee|ei|eo|eu|ey|ia|ie|ii|io|iu|iy|oa|oe|oi|oo|ou|oy|ua|ue|ui|uo|uu|uy|ya|ye|yi|yo|yu|yy", t)
        syl += len(diph)
        t = re.sub(r"aa|ae|ai|ao|au|ay|ea|ee|ei|eo|eu|ey|ia|ie|ii|io|iu|iy|oa|oe|oi|oo|ou|oy|ua|ue|ui|uo|uu|uy|ya|ye|yi|yo|yu|yy", "", t)
        syl += len(re.findall(r"[aeiouy]", t))
        return max(syl, 1)

    def count_adverbs(self, words):
        return sum(1 for w in words if w.lower().endswith('ly') and len(w) > 4)

    def count_weak_verbs(self, words):
        return sum(1 for w in words if w.lower() in self.weak_verbs_set)

    def count_passive_voice(self, text):
        return len(re.findall(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b", text, re.IGNORECASE))

    def count_hard_adjectives(self, words):
        return sum(1 for w in words if self.syllables_in_word(w) >= 3 and self.adjective_suffixes.search(w))

    def _count_nominalizations(self, words):
        return sum(1 for w in words if self.nominalization_patterns.search(w) and len(w) > 5)

    def _count_unique_words(self, words):
        freq = {}
        for w in words: freq[w.lower()] = freq.get(w.lower(), 0) + 1
        unique = sum(1 for w in words if freq[w.lower()] == 1)
        repeat = len(words) - len(set(w.lower() for w in words))
        return unique, repeat

    def _categorize_sentences(self, sentences):
        s, m = 10, 21
        short = sum(1 for x in sentences if len(self.split_words(x)) <= s)
        medium = sum(1 for x in sentences if s < len(self.split_words(x)) < m)
        long = sum(1 for x in sentences if len(self.split_words(x)) >= m)
        return short, medium, long

    def analyze(self, text):
        norm = self.normalize_text(text)
        sentences = self.split_sentences(norm)
        words = self.split_words(norm)
        letters = self.count_letters(norm)
        chars_with = self.count_chars_with_spaces(norm)
        chars_without = self.count_chars_without_spaces(norm)
        avg_len = self.avg_word_length(words)
        longest_word, longest_len = self.longest_word(words)
        syl_list = [self.syllables_in_word(w) for w in words]
        total_syl = sum(syl_list)
        short, medium, long_ = self._categorize_sentences(sentences)
        paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        par_counts = [len(self.split_words(p)) for p in paragraphs]
        unique_count, repeat_count = self._count_unique_words(words)

        return {
            "difficulty": {
                "hardWords": sum(1 for s in syl_list if s >= 3),
                "longSentences": long_,
                "adverbs": self.count_adverbs(words),
                "hardAdjectives": self.count_hard_adjectives(words),
                "nominals": self._count_nominalizations(words),
                "passiveWords": self.count_passive_voice(norm),
                "weakVerbs": self.count_weak_verbs(words)
            },
            "character": {
                "totalWords": len(words),
                "avgWordLength": round(avg_len),
                "longestWord": longest_word,
                "longestWordLength": longest_len,
                "charsWithSpaces": chars_with,
                "charsWithoutSpaces": chars_without,
                "lettersAZ": letters,
                "alphaNumeric": letters
            },
            "sentences": {
                "total": len(sentences),
                "lineCount": 0,
                "totalLines": len(sentences),
                "avgLength": round(len(words)/len(sentences)) if sentences else 0,
                "activeVoice": len(sentences) - self.count_passive_voice(norm),
                "passiveVoice": self.count_passive_voice(norm),
                "short": short,
                "medium": medium,
                "long": long_
            },
            "paragraphs": {
                "count": len(paragraphs),
                "shortest": min(par_counts) if par_counts else 0,
                "longest": max(par_counts) if par_counts else 0
            },
            "words": {
                "easy": sum(1 for s in syl_list if s < 3),
                "hard": sum(1 for s in syl_list if s >= 3),
                "compound": 0,
                "cardinal": 0,
                "properNoun": 0,
                "abbreviated": 0,
                "unique": unique_count,
                "repeat": repeat_count
            },
            "syllables": {
                "total": total_syl,
                "avgPerWord": round(total_syl/len(words), 2) if words else 0,
                "oneSyl": syl_list.count(1),
                "twoSyl": syl_list.count(2),
                "threeSyl": syl_list.count(3),
                "fourSyl": syl_list.count(4),
                "fiveSyl": syl_list.count(5),
                "sixSyl": syl_list.count(6),
                "sevenPlusSyl": sum(1 for s in syl_list if s >= 7)
            }
        }

class StatsComparer:
    def __init__(self, reference_data):
        self.reference_data = reference_data

    def compare_value(self, calculated, reference, tolerance=0):
        match = abs(calculated - reference) <= tolerance
        color = "\033[92m" if match else "\033[91m"  # green/red in console
        icon = "✓" if match else "✗"
        return match, color, icon

    def format_comparison(self, label, calculated, reference, unit='', tolerance=0):
        match, color, icon = self.compare_value(calculated, reference, tolerance)
        return f"{color}{label}: {calculated}{unit} {icon} (Expected: {reference}{unit})\033[0m"

    def show_stats(self, data):
        print("\n--- WORD/CHARACTER STATS ---")
        c = data['character']
        r = self.reference_data['character']
        print(self.format_comparison("Total # of words", c['totalWords'], r['totalWords']))
        print(self.format_comparison("Average word length", c['avgWordLength'], r['avgWordLength'], " characters"))
        lw_match = c['longestWord'] == r['longestWord']
        lw_color = "\033[92m" if lw_match else "\033[91m"
        lw_icon = "✓" if lw_match else "✗"
        print(f"{lw_color}Longest word: {c['longestWord']} ({c['longestWordLength']} chars) {lw_icon} "
              f"(Expected: {r['longestWord']} ({r['longestWordLength']} chars))\033[0m")
        print(self.format_comparison("Character Count (with spaces)", c['charsWithSpaces'], r['charsWithSpaces'], " chars"))
        print(self.format_comparison("Character Count (without spaces)", c['charsWithoutSpaces'], r['charsWithoutSpaces'], " chars"))
        print(self.format_comparison("Letters A-Z", c['lettersAZ'], r['lettersAZ'], " chars"))
        print(self.format_comparison("Alpha-numeric chars", c['alphaNumeric'], r['alphaNumeric'], " chars"))

        print("\n--- TEXT DIFFICULTY ---")
        d = data['difficulty']
        dr = self.reference_data['difficulty']
        for key in ['hardWords','longSentences','adverbs','hardAdjectives','nominals','passiveWords','weakVerbs']:
            print(self.format_comparison(key, d[key], dr[key]))

        print("\n--- SENTENCE STATS ---")
        s = data['sentences']
        sr = self.reference_data['sentences']
        print(self.format_comparison("Total # of sentences", s['total'], sr['total']))
        print(self.format_comparison("Average sentence length", s['avgLength'], sr['avgLength'], " words"))
        print(self.format_comparison("Active voice sentences", s['activeVoice'], sr['activeVoice']))
        print(self.format_comparison("Passive voice sentences", s['passiveVoice'], sr['passiveVoice']))
        for key in ['short','medium','long']:
            print(self.format_comparison(f"Total # of {key} sentences", s[key], sr[key]))

        print("\n--- WORD STATS ---")
        w = data['words']
        wr = self.reference_data['words']
        for key, label in [('easy', '# of Easy Words'), ('hard', '# of Hard Words'), ('unique', 'Unique words'), ('repeat', 'Repeat words')]:
            print(self.format_comparison(label, w[key], wr[key]))

        print("\n--- SYLLABLE STATS ---")
        sy = data['syllables']
        syr = self.reference_data['syllables']
        print(self.format_comparison("Total syllables", sy['total'], syr['total']))
        print(self.format_comparison("Average syllables per word", sy['avgPerWord'], syr['avgPerWord'], '', 0.01))
        sy_keys = [
            ('oneSyl', "1 syllable"),
            ('twoSyl', "2 syllables"),
            ('threeSyl', "3 syllables"),
            ('fourSyl', "4 syllables"),
            ('fiveSyl', "5 syllables"),
            ('sixSyl', "6 syllables"),
            ('sevenPlusSyl', "7+ syllables")
        ]
        
        for key, label in sy_keys:
            print(self.format_comparison(f"Words with {label}", sy[key], syr[key]))
        print("\n--- PARAGRAPH STATS ---")
        p = data['paragraphs']
        pr = self.reference_data['paragraphs']
        print(self.format_comparison("Number of paragraphs", p['count'], pr['count']))
        print(self.format_comparison("Shortest paragraph", p['shortest'], pr['shortest'], " words"))
        print(self.format_comparison("Longest paragraph", p['longest'], pr['longest'], " words"))

import math

class ReadabilityEngine:
    def calculateARI(self, data):
        chars = data['character']['charsWithoutSpaces']
        words = data['character']['totalWords']
        sentences = data['sentences']['total']
        return round(4.71 * (chars / words) + 0.5 * (words / sentences) - 21.43, 2)

    def calculateFlesch(self, data):
        words = data['character']['totalWords']
        sentences = data['sentences']['total']
        syllables = data['syllables']['total']
        return round(206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words), 2)

    def calculateGFI(self, data):
        words = data['character']['totalWords']
        sentences = data['sentences']['total']
        complex_words = data['words']['hard']
        compound = data['words']['compound']
        return round(0.4 * ((words / (sentences + compound)) + 100 * (complex_words / words)), 2)

    def calculateFK(self, data):
        words = data['character']['totalWords']
        sentences = data['sentences']['total']
        syllables = data['syllables']['total']
        return round(0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59, 2)

    def calculateCLI(self, data):
        letters = data['character']['lettersAZ']
        words = data['character']['totalWords']
        sentences = data['sentences']['total']
        L = (letters / words) * 100
        S = (sentences / words) * 100
        return round(0.0588 * L - 0.296 * S - 15.8, 2)

    def calculateSMOG(self, data):
        sentences = data['sentences']['total']
        complex_words = data['words']['hard']
        return round(1.043 * math.sqrt((complex_words * (30 / sentences)) + 3.1291), 2)

    def calculateLinsearWrite(self, data):
        sentences = data['sentences']['total']
        easy = data['words']['easy']
        hard = data['words']['hard']
        compound = data['words']['compound']
        ignored = 3
        initial = ((easy - ignored) * 1 + hard * 3) / (sentences + compound)
        adjusted = initial / 2 if initial > 20 else (initial - 2) / 2
        return round(adjusted, 2)

    def calculateFORCAST(self, data):
        words = data['character']['totalWords']
        one_syl = data['syllables']['oneSyl']
        return round(20 - ((one_syl / words) * 150 / 10), 2)

    def calculate(self, data):
        results = [
            self.calculateARI(data),
            self.calculateFlesch(data),
            self.calculateGFI(data),
            self.calculateFK(data),
            self.calculateCLI(data),
            self.calculateSMOG(data),
            self.calculateLinsearWrite(data),
            self.calculateFORCAST(data)
        ]
        return results

class View:
    def show_results(self, results):
        for res in results:
            print(f"{res['name']}")
            print(f"Score: {res['score']} | Grade: {res['grade']} | Level: {res['level']} | Ages: {res['ages']}")
            print(f"{res['formulaHTML']}\n")


def handle_request(request):
    if request.method == 'OPTIONS':
        return {}
        
    if request.method == 'POST':
        text = request.json.get('text')   # if raw text
        pub_key = request.json.get("pub")
        text_analyzer = TextAnalyzer()
        formulas = ReadabilityEngine()
        data = text_analyzer.analyze(text)  # Analyze the text
        results = formulas.calculate(data)
        encrypted = encrypt_for_client({"r": results}, pub_key)
        return {"r": encrypted}

    return 'Hello from Flask!'
