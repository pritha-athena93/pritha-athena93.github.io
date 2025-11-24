# Extract Resume Text from PDF

Since you want to use a text document instead of PDF, you have a few options:

## Option 1: Extract Text from Existing PDF

You can extract the text from your existing PDF:

### Using Python:
```bash
cd /Users/pritha/playground/career-agent/backend
python3 -c "
from PyPDF2 import PdfReader
reader = PdfReader('../resume.pdf')
text = '\n\n'.join([page.extract_text() for page in reader.pages])
with open('resume.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print('Resume extracted to resume.txt')
"
```

### Using macOS Preview:
1. Open `resume.pdf` in Preview
2. Select All (Cmd+A)
3. Copy (Cmd+C)
4. Paste into a text editor
5. Save as `backend/resume.txt`

### Using Online Tools:
- Upload PDF to any PDF-to-text converter
- Copy the text
- Save as `backend/resume.txt`

## Option 2: Create Resume Manually

1. Open `backend/resume.txt` in a text editor
2. Paste or type your resume content
3. Save the file

## Option 3: Use Markdown Format

You can also use `resume.md` for Markdown formatting:
- Supports headers, lists, bold, italic
- More readable and structured

## After Creating resume.txt

1. The backend will automatically use it
2. Deploy: `./scripts/deploy-backend.sh`
3. The AI will answer questions based on the text content

## File Location

Place your resume text file in:
- `backend/resume.txt` (preferred)
- OR `backend/resume.md` (Markdown format)

The backend will automatically find and load it.


