# Interview Transcript Summarizer

A command-line Python script that reads an interview transcript and produces a structured candidate summary covering topics discussed, candidate profile, and a hiring assessment.

---

## Requirements

- Python 3.8 or above
- A free Groq API key

---

## Setup

**Step 1. Install the dependency**

```bash
pip install groq
```

**Step 2. Get a Groq API key**

Go to [https://console.groq.com](https://console.groq.com), sign up with email or Google, and create a key under the API Keys section. It is free and does not require a credit card.

**Step 3. Set the API key**

Mac or Linux:
```bash
export GROQ_API_KEY=your_key_here
```

Windows (Command Prompt):
```cmd
set GROQ_API_KEY=your_key_here
```

Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your_key_here"
```

Or create a `.env` file in the project root and add this line:
```
GROQ_API_KEY=your_key_here
```
Then run `source .env` before the script. The `.env` file is in `.gitignore` and will not be committed.

---

## How to run

```bash
python summarizer.py sample_transcript_assignment_1.txt
python summarizer.py sample_transcript_assignment_2.txt
```

The summary prints directly to the terminal in this format:

```
============================================================
INTERVIEW SUMMARY
============================================================

TOPICS COVERED
...

CANDIDATE PROFILE
...

CANDIDATE SUMMARY
...

============================================================
```

---

## Project files

```
interview-summarizer/
├── summarizer.py                        # Main script
├── prompt_iterations.md                 # Three prompt iterations with outputs
├── README.md                            # This file
├── .gitignore
├── sample_transcript_assignment_1.txt
└── sample_transcript_assignment_2.txt
```

---

## Provider and model

Provider: **Groq**
Model: **llama-3.3-70b-versatile**

Groq was chosen for its fast inference and generous free tier (1,000 requests per day, no credit card needed). The 70b Llama 3.3 model handles both technical and non-technical transcripts reliably and produces well-structured output with a clear system instruction.

---

## Reflection

**What surprised me**

The biggest surprise was how much the negative constraints mattered. Early prompt versions produced uniformly positive, hedged summaries because the model defaults toward encouragement when not given other instructions. Adding explicit rules like "do not fill gaps with generic praise" and "a candidate who is strong in some areas but weak in others should not read as universally impressive" was what finally produced honest, balanced summaries. Positive framing instructions alone were not enough.

The second thing that surprised me was how differently the two transcripts needed to be handled. Transcript 1 had a live coding failure that needed to be surfaced directly. Transcript 2 had confident, detailed answers but a nuanced flag from the interviewer at the very end about language use under pressure. Getting a single prompt to handle both without flattening them into the same shape took more iteration than expected.

**What I would improve with another day**

The current script generates a full three-section output regardless of transcript length. For very short transcripts (under 400 words), the output can feel padded. A word count check that either shortens the expected output or flags the transcript as too thin would help at the edges.

A fourth output section would also be useful: a short list of suggested follow-up questions based on gaps or unclear areas in the transcript, making the output directly actionable for the next interview round.

**Limitations of the final prompt**

The prompt instructs the model to stay grounded in the transcript, but it cannot verify whether candidate claims are accurate. When a candidate gives detailed, confident answers (as in Transcript 2), the model may treat those as established facts rather than self-reported claims. Summaries should be read as based on what the candidate said, not as independently verified assessments.

The prompt also works best on English-language transcripts. Interviews with heavy code-switching or regional idioms may produce less reliable output. Finally, if the interviewer asked poor questions or the candidate gave very short answers, the output will reflect that, which is technically correct but may feel unhelpful to someone expecting depth from thin material.
