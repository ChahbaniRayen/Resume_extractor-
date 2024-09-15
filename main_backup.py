import spacy
from spacy.matcher import Matcher
from skills import skill_patterns
from jobs import job_patterns
from studies import education_patterns
import re

# Load the spaCy model

data = {
    "full_name": "",
    "location": "",
    "phone_number": "",
    "email": "",
    "professional_experience": [],
    "skills": set(),
    "education": [],
}


class ResumeExtractor:
    phone_regexs = [
        r"(\+\d{1,3}\s?)?(\d{2,3}\s?){4,5}",  # General pattern for international and local phone numbers
    ]
    email_regex = r"[\w\.-]+@[\w\.-]+\.\w+"  # General pattern for email addresses

    def __init__(self, nlp, skill_patterns):
        self.nlp = nlp
        self.skill_matcher = Matcher(nlp.vocab)
        self.job_matcher = Matcher(nlp.vocab)
        self.edu_matcher = Matcher(nlp.vocab)
        self.skill_matcher.add("SKILL", skill_patterns)
        self.job_matcher.add("JOB", job_patterns)
        self.edu_matcher.add("EDU", education_patterns)

    def extract(self, text):
        doc = self.nlp(text)
        self.extract_skills(doc)
        self.extract_jobs(doc)
        self.extract_studies(doc)
        self.extract_entities(doc)
        self.extract_phone_numbers(doc.text)
        self.extract_emails(doc.text)
        self.clean_data()
        return data

    def clean_data(self):
        data["full_name"] = data["full_name"].strip()
        data["location"] = data["location"].strip()
        data["phone_number"] = data["phone_number"].strip()
        data["email"] = data["email"].strip()
        # remove empty strings and if the string ends with "for" or "of"

        data["professional_experience"] = [
            job.strip()
            for job in list(set(data["professional_experience"]))
            if job.strip()
            and not (
                job.strip().lower().endswith("for")
                or job.strip().lower().endswith("of")
            )
        ]
        data["skills"] = [
            skill.strip()
            for skill in list(set(data["skills"]))
            if skill.strip()
            and not (
                skill.strip().lower().endswith("for")
                or skill.strip().lower().endswith("of")
            )
        ]
        data["education"] = [
            edu.strip()
            for edu in list(set(data["education"]))
            if edu.strip()
            and not (
                edu.strip().lower().endswith("for")
                or edu.strip().lower().endswith("of")
            )
        ]

    def extract_skills(self, doc):
        matches = self.skill_matcher(doc)
        for match_id, start, end in matches:
            data["skills"].add(doc[start:end].text)

    def extract_jobs(self, doc):
        matches = self.job_matcher(doc)
        for match_id, start, end in matches:
            data["professional_experience"].append(doc[start:end].text)

    def extract_studies(self, doc):
        matches = self.edu_matcher(doc)
        for match_id, start, end in matches:
            data["education"].append(doc[start:end].text)

    def extract_entities(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not data["full_name"]:
                data["full_name"] = ent.text.strip()
            elif ent.label_ == "GPE":
                data["location"] = ent.text.strip()
            elif ent.label_ == "ORG":
                data["professional_experience"].append(ent.text.strip())
            elif ent.label_ == "EDU":
                data["education"].append(ent.text.strip())

    def extract_phone_numbers(self, text):
        for regex in self.phone_regexs:
            match = re.search(regex, text)
            if match:
                data["phone_number"] = match.group().strip()
                break

    def extract_emails(self, text):
        match = re.search(self.email_regex, text)
        if match:
            data["email"] = match.group().strip()


# Initialize the extractor
nlp = spacy.load("en_core_web_sm")

extractor = ResumeExtractor(nlp, skill_patterns)

# Example resume text
resume_text = """
John Doe
Paris, France
+216 99 999 999
test@test.com

Professional Experience:
- Software Developer at TechCorp
- Web Developer at WebInnovate

Education:
- Master of Computer Science at University of Paris
- Bachelor of Computer Science at University of Paris

Skills:
- Python
- JavaScript
- React
"""

# Extract information
info = extractor.extract(resume_text)
print(info)
