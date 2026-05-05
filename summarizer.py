import os
import sys
from pathlib import Path
from groq import Groq

SYSTEM_PROMPT = """You are a senior technical recruiter and talent analyst with 15 years of experience
evaluating candidates across engineering, product, and operations roles. You read interview transcripts
carefully and produce structured, honest, and useful summaries for hiring teams.

Your summaries must be grounded strictly in what the transcript shows. Do not invent or assume skills
or experiences not evidenced in the conversation. If the transcript is short or vague on a dimension,
say so honestly rather than filling gaps with generic praise.

You write in clear, direct English. No filler phrases like "the candidate demonstrated a strong passion
for" or "showcases exceptional talent." Be specific. Reference actual moments from the transcript when
relevant."""

USER_PROMPT = """Read the following interview transcript carefully, then produce a structured candidate
summary with exactly three sections.

--- TRANSCRIPT START ---
{transcript}
--- TRANSCRIPT END ---

Write the structured summary using this exact format. Do not add extra sections or change the headers.

TOPICS COVERED
List the main themes and subject areas discussed in this interview. For each topic, write one line:
the topic name followed by a colon and a brief note on what was actually covered. Aim for 4 to 8
topics. Focus on what was substantively discussed, not just briefly mentioned.

CANDIDATE PROFILE
State the role and seniority level this candidate fits, for example "Backend Engineer, mid-level" or
"Operations Program Manager, mid-senior." Follow with 3 to 5 sentences of justification. Be specific:
cite years of experience, tools named, depth of answers, or gaps observed. If the transcript is from
a non-technical role, assess communication clarity, process thinking, and leadership indicators.

CANDIDATE SUMMARY
Write a single paragraph of 4 to 6 sentences. Cover: (1) professional background and experience span,
(2) two or three concrete technical or functional strengths, (3) one or two honest concerns or
limitations visible in the transcript, (4) an overall hiring impression. Be balanced. A candidate who
is strong in some areas but weak in others should not read as universally impressive or universally
weak."""


def summarize(transcript_path):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.")
        sys.exit(1)

    transcript = Path(transcript_path).read_text(encoding="utf-8").strip()

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT.format(transcript=transcript)},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    result = response.choices[0].message.content.strip()

    print("\n" + "=" * 60)
    print("INTERVIEW SUMMARY")
    print("=" * 60 + "\n")
    print(result)
    print("\n" + "=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <transcript_file>")
        sys.exit(1)
    summarize(sys.argv[1])
