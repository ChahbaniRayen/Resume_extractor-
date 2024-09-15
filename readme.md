# Resume Information Extractor API

The Resume Information Extractor API is designed to extract key information from resumes, such as personal details, professional experience, skills, and educational background. This API accepts PDF documents, processes the text within, and extracts structured information using Natural Language Processing (NLP) techniques powered by spaCy and custom-defined patterns.

## Features

- Extracts personal information like full name, location, phone number, and email address.
- Identifies professional experiences including job titles and organizations.
- Recognizes skills and technical proficiencies.
- Extracts educational qualifications, fields of study, and institutions.

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip and venv

### Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create and activate a virtual environment:

   - On Windows:

     ```sh
     python -m venv venv
     .\venv\Scripts\activate
     ```

   - On Unix or MacOS:

     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install the dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Download the necessary spaCy language model:

   ```sh
   python -m spacy download en_core_web_sm
   ```

   better to use the following model but it's too large
   ```sh
    python -m spacy download en_core_web_lg or en_core_web_trf
    ```

### Running the Server

Launch the Flask application by running:

```sh
flask run
```

This command starts a local development server on `http://localhost:5000`.

## API Usage

### Endpoint: Extract Resume Information

- **URL**: `/extract_resume`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**: A file with the key `file`, containing the resume in PDF format.

#### Example Request

Using `curl` from the command line:

```sh
curl -X POST -F 'file=@/path/to/resume.pdf' http://localhost:5000/extract_resume
```

```typescript
import axios from 'axios';
import * as fs from 'fs';


const resumeFile = fs.readFileSync('/path/to/resume.pdf');


const formData = new FormData();
formData.append('file', resumeFile);

axios.post('http://localhost:5000/extract_resume', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
```


#### Response

The API returns a JSON object containing extracted information, structured as follows:

```json
{
  "full_name": "John Doe",
  "location": "France",
  "phone_number": "+216 99 999 999",
  "email": "test@test.com",
  "professional_experience": [
    "Software Developer at TechCorp",
    "Web Developer at WebInnovate"
  ],
  "skills": [
    "Python",
    "JavaScript",
    "React"
  ],
  "education": [
    "Master of Computer Science at University of Paris",
    "Bachelor of Computer Science at University of Paris"
  ]
}
```
# Resume_extractor-
