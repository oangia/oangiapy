text = "Learning to code is an essential skill in todays world. It allows people to create software automate tasks and solve complex problems efficiently. Beginners may feel overwhelmed at first but with consistent practice even challenging concepts become manageable. Programming languages vary in syntax and complexity yet the fundamental logic remains similar across most languages. Understanding algorithms data structures and design patterns is crucial for building reliable and scalable applications. Moreover coding fosters critical thinking problem solving and creativity. Online tutorials coding bootcamps and practice projects provide ample opportunities for learners to improve and gain confidence in their abilities."
text_analyzer = TextAnalyzer()
formulas = ReadabilityEngine()

data = text_analyzer.analyze(text)  # Analyze the text

# Optional: show character/difficulty/syllable stats (like showStats in JS)
# comparer = StatsComparer(TextAnalyzer.REFERENCE_DATA)
# comparer.show_stats(data)

results = formulas.calculate(data)  # Calculate readability scores

# Print results
for res in results:
    print(f"{res['name']}: Score={res['score']}, Level={res['level']}, Grade={res['grade']}, Ages={res['ages']}")
    print(f"Formula: {res['formulaHTML']}\n")

comparer = StatsComparer(TextAnalyzer.REFERENCE_DATA)
comparer.show_stats(data)
