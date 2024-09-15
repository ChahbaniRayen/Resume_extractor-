from spacy.matcher import Matcher
from skills import skill_patterns
from jobs import job_patterns
from studies import education_patterns
import re

# Load the spaCy model


class ResumeExtractor:
    phone_regexs = [
        r"(\+\d{1,3}\s?)?(\d{2,3}\s?){4,5}",  # General pattern for international and local phone numbers
    ]
    email_regex = r"[\w\.-]+@[\w\.-]+\.\w+"  # General pattern for email addresses

    def __init__(self, nlp):
        self.nlp = nlp
        self.data = {
            "full_name": "",
            "location": "",
            "phone_number": "",
            "email": "",
            "professional_experience": [],
            "skills": set(),
            "education": [],
        }
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
        return self.data

    def clean_data(self):
        self.data["full_name"] = self.data["full_name"].strip()
        self.data["location"] = self.data["location"].strip()
        self.data["phone_number"] = self.data["phone_number"].strip()
        self.data["email"] = self.data["email"].strip()
        # remove empty strings and if the string ends with "for" or "of"

        self.data["professional_experience"] = [
            job.strip()
            for job in list(set(self.data["professional_experience"]))
            if job.strip()
            and not (
                job.strip().lower().endswith("for")
                or job.strip().lower().endswith("of")
            )
        ]
        self.data["skills"] = [
            skill.strip()
            for skill in list(set(self.data["skills"]))
            if skill.strip()
            and not (
                skill.strip().lower().endswith("for")
                or skill.strip().lower().endswith("of")
            )
        ]
        self.data["education"] = [
            edu.strip()
            for edu in list(set(self.data["education"]))
            if edu.strip()
            and not (
                edu.strip().lower().endswith("for")
                or edu.strip().lower().endswith("of")
            )
        ]

    def extract_skills(self, doc):
        matches = self.skill_matcher(doc)
        for match_id, start, end in matches:
            self.data["skills"].add(doc[start:end].text)

    def extract_jobs(self, doc):
        matches = self.job_matcher(doc)
        for match_id, start, end in matches:
            self.data["professional_experience"].append(doc[start:end].text)

    def extract_studies(self, doc):
        matches = self.edu_matcher(doc)
        for match_id, start, end in matches:
            self.data["education"].append(doc[start:end].text)

    def extract_entities(self, doc):
        for ent in doc.ents:
            if ent.label_ == "PERSON" and not self.data["full_name"]:
                self.data["full_name"] = ent.text.strip()
            elif ent.label_ == "GPE":
                self.data["location"] = ent.text.strip()
            elif ent.label_ == "ORG":
                self.data["professional_experience"].append(ent.text.strip())
            elif ent.label_ == "EDU":
                self.data["education"].append(ent.text.strip())

    def extract_phone_numbers(self, text):
        for regex in self.phone_regexs:
            match = re.search(regex, text)
            if match:
                self.data["phone_number"] = match.group().strip()
                break

    def extract_emails(self, text):
        match = re.search(self.email_regex, text)
        if match:
            self.data["email"] = match.group().strip()
