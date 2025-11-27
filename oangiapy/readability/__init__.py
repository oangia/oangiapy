import re
import json
import unicodedata
import math
from oangiapy.crypto import Crypto

class TextAnalyzer:
    def __init__(self):
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

class ReadabilityEngine:
    def __init__(self, text):
        text_analyzer = TextAnalyzer()
        self.data = text_analyzer.analyze(text)  # Analyze the text
        
    def calcARI(self):
        chars = self.data['character']['charsWithoutSpaces']
        words = self.data['character']['totalWords']
        sentences = self.data['sentences']['total']
        return round(4.71 * (chars / words) + 0.5 * (words / sentences) - 21.43, 2)

    def calcFlesch(self):
        words = self.data['character']['totalWords']
        sentences = self.data['sentences']['total']
        syllables = self.data['syllables']['total']
        return round(206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words), 2)

    def calcGFI(self):
        words = self.data['character']['totalWords']
        sentences = self.data['sentences']['total']
        complex_words = self.data['words']['hard']
        compound = self.data['words']['compound']
        return round(0.4 * ((words / (sentences + compound)) + 100 * (complex_words / words)), 2)

    def calcFK(self):
        words = self.data['character']['totalWords']
        sentences = self.data['sentences']['total']
        syllables = self.data['syllables']['total']
        return round(0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59, 2)

    def calcCLI(self):
        letters = self.data['character']['lettersAZ']
        words = self.data['character']['totalWords']
        sentences = self.data['sentences']['total']
        L = (letters / words) * 100
        S = (sentences / words) * 100
        return round(0.0588 * L - 0.296 * S - 15.8, 2)

    def calcSMOG(self):
        sentences = self.data['sentences']['total']
        complex_words = self.data['words']['hard']
        return round(1.043 * math.sqrt((complex_words * (30 / sentences)) + 3.1291), 2)

    def calcLinsearWrite(self):
        sentences = self.data['sentences']['total']
        easy = self.data['words']['easy']
        hard = self.data['words']['hard']
        compound = self.data['words']['compound']
        ignored = 3
        initial = ((easy - ignored) * 1 + hard * 3) / (sentences + compound)
        adjusted = initial / 2 if initial > 20 else (initial - 2) / 2
        return round(adjusted, 2)

    def calcFORCAST(self):
        words = self.data['character']['totalWords']
        one_syl = self.data['syllables']['oneSyl']
        return round(20 - ((one_syl / words) * 150 / 10), 2)

    def calculate(self):
        results = [
            self.calcARI(),
            self.calcFlesch(),
            self.calcGFI(),
            self.calcFK(),
            self.calcCLI(),
            self.calcSMOG(),
            self.calcLinsearWrite(),
            self.calcFORCAST()
        ]
        return results
  
def analyze(adapter):
    data = adapter.get_data()
    ip = adapter.get_client_ip()
    text = data.get("text")
    pub_key = data.get("pub")
    length = len(text)
    if length < 100 or length > 1000:
        return {'error': 'Input text must between 100 and 1000 characters long.'}, 400
    
    engine = ReadabilityEngine(text)
    encrypted = Crypto.rsa_encrypt({"fomulas": engine.calculate()}, pub_key)
    ip = Crypto.rsa_encrypt({"ip": ip}, pub_key)
    return {"f": encrypted, "i": ip}, 200
