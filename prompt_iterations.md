# Prompt Iterations

This log documents the three main prompt versions I worked through while building the transcript summarizer. I tested every version against both transcripts (Transcript 1: Prasanna, a frontend/mobile engineer; Transcript 2: Krishna, an operations/program manager). The two transcripts are meaningfully different in domain, communication style, and depth of answers, so they served as a good stress test.

---

## Iteration 1

### The Prompt

```
You are a recruiter assistant. Read this interview transcript and give me:
1. Topics covered
2. Candidate profile (role and level)
3. A short summary of the candidate

Transcript:
{transcript}
```

### Input Used

Full transcript for both runs (Transcript 1 ~900 words, Transcript 2 ~1100 words).

### Output (Transcript 1 excerpt)

```
Topics Covered:
- AI-assisted development
- Mobile app development
- React and Angular
- Capacitor/Ionic
- CSS and Tailwind
- State management

Candidate Profile:
Prasanna appears to be a mid-level frontend developer with experience in React and Angular.

Candidate Summary:
Prasanna has around 9 years of experience working on frontend applications using Angular, React,
and Ionic. He seems knowledgeable about mobile development and AI tools. Overall a decent candidate.
```

### Output (Transcript 2 excerpt)

```
Topics Covered:
- Vendor management
- Fraud detection
- Operations
- Stakeholder management

Candidate Profile:
Krishna seems to be a program manager or operations lead.

Candidate Summary:
Krishna has worked in ed-tech operations and has experience with fraud detection and CRM
implementation. He appears to be a capable operations professional.
```

### What Worked / What Did Not

The basic structure came through fine, three sections, readable output. But the role classification on Transcript 1 was wrong: it called Prasanna a "Full Stack Engineer" when the entire interview was frontend-heavy, because I gave the model no instruction to analyze what the interview actually tested versus what was on the resume. On Transcript 2, the summary invented a "willingness to learn" trait that never appeared in the conversation. That told me the prompt needed two things for version 2: a hard constraint against inventing traits, and a longer justification requirement to force real reasoning about the interview content.

---

## Iteration 2

### The Prompt

```
You are a senior technical recruiter with 10 years of experience. Read the interview transcript
below and produce a structured candidate summary with three sections:

1. TOPICS COVERED: List the main themes discussed (4-8 topics), one per line.

2. CANDIDATE PROFILE: State the role and level (e.g. "Backend Engineer, mid-level"). Justify
in 2-3 sentences based on the transcript.

3. CANDIDATE SUMMARY: A paragraph of 4-5 sentences covering background, strengths, weaknesses,
and overall impression. Be honest and specific, not generic.

Do not invent skills not mentioned in the transcript. If something is unclear, say so.

Transcript:
{transcript}
```

### Input Used

Full transcript for both runs.

### Output (Transcript 1 excerpt)

```
TOPICS COVERED
- AI-assisted development (Cursor, GitHub Copilot, Claude for code generation)
- Ionic framework and mobile dashboard development
- Capacitor plugins: camera, filesystem, network
- Tailwind CSS and responsive design systems
- Angular modular architecture
- React state management (Context API, React Query, Redux)
- Live coding: Zustand store, Redux slice

CANDIDATE PROFILE
Frontend/Mobile Engineer, mid-level. Prasanna has 9 years of experience with a clear focus
on Angular, React, and Ionic. His answers showed breadth across the stack but struggled on
live coding tasks like Zustand and Redux slice.

CANDIDATE SUMMARY
Prasanna brings solid hands-on experience across Angular, React, and Ionic with a good grasp
of mobile development patterns including Capacitor plugins. He is comfortable using AI coding
assistants as part of his workflow. However, his live coding answers were hesitant and incomplete,
and his verbal explanations were sometimes hard to follow. He would likely need a structured
onboarding environment and close collaboration rather than independent ownership of features.
```

### Output (Transcript 2 excerpt)

```
TOPICS COVERED
- Fraud detection system built from scratch
- Vendor onboarding and management
- Stakeholder and leadership communication
- CRM implementation
- BPO/calling operations optimization
- KPI tracking and executive reporting
- Prioritization under competing stakeholder demands
- Data presentation and handling disagreements

CANDIDATE PROFILE
Operations Program Manager, mid-senior. Krishna has 5+ years in ed-tech operations with
clear ownership of complex cross-functional projects. His answers showed real depth on
vendor management, data analysis, and process design.

CANDIDATE SUMMARY
Krishna has built meaningful operational systems from scratch including a fraud risk scoring
model, CRM migration, and BPO dialer optimization. He thinks in structured frameworks and
communicates decision-making logic clearly. A notable flag from the interviewer is his use
of Hindi jargon under pressure, which may be a concern for senior stakeholder presentations.
Overall he comes across as a high-initiative operator who would be strong in execution-heavy
roles.
```

### What Worked / What Did Not

The hallucination problem largely went away once I added "do not invent skills not mentioned in the transcript," and the Transcript 2 profile became noticeably more grounded, citing the 22-vendor pan-India detail specifically. But Transcript 1 still came back as "Full Stack Engineer," which told me the 2-3 sentence justification cap was too short to push the model past surface-level resume scanning. I also noticed the Transcript 2 profile said the candidate had "the ability to communicate complex ideas" and then flagged communication as a concern in the very next line, a contradiction the prompt had no way to prevent. For version 3 I needed a longer justification window, a system prompt to lock in an evaluative voice, and explicit criteria for assessing non-technical candidates so the model stopped improvising on Transcript 2.

---

## Iteration 3 (Final)

### The Prompt

**System instruction (passed separately via the API's system_instruction field):**

```
You are a senior technical recruiter and talent analyst with 15 years of experience evaluating
candidates across engineering, product, and operations roles. You read interview transcripts
carefully and produce structured, honest, and useful summaries for hiring teams.

Your summaries must be grounded strictly in what the transcript shows. Do not invent or assume
skills or experiences not evidenced in the conversation. If the transcript is short or vague on
a dimension, say so honestly rather than filling gaps with generic praise.

You write in clear, direct English. No filler phrases like "the candidate demonstrated a strong
passion for" or "showcases exceptional talent." Be specific. Reference actual moments from the
transcript when relevant.
```

**User prompt:**

```
Read the following interview transcript carefully, then produce a structured candidate summary
with exactly three sections.

--- TRANSCRIPT START ---
{transcript}
--- TRANSCRIPT END ---

Now write the structured summary using this exact format. Do not add extra sections or change
the section headers.

TOPICS COVERED
List the main themes and subject areas discussed in this interview. For each topic, write one
line: the topic name followed by a colon and a brief note on what was actually covered. Aim for
4 to 8 topics. Focus on what was substantively discussed, not just briefly mentioned.

CANDIDATE PROFILE
State the role and seniority level this candidate fits, for example "Backend Engineer, mid-level"
or "Operations Program Manager, mid-senior." Follow with 3 to 5 sentences of justification. Be
specific: cite years of experience, tools named, depth of answers, or gaps observed. If the
transcript is from a non-technical role, assess communication clarity, process thinking, and
leadership indicators.

CANDIDATE SUMMARY
Write a single paragraph of 4 to 6 sentences. Cover: (1) professional background and experience
span, (2) two or three concrete technical or functional strengths, (3) one or two honest concerns
or limitations visible in the transcript, (4) an overall hiring impression. Be balanced. A
candidate who is strong in some areas but weak in others should not read as universally impressive
or universally weak.
```

### Input Used

Full transcript for both runs.

### Output (Transcript 1)

```
TOPICS COVERED
AI-assisted development: Candidate described integrating Cursor, GitHub Copilot, and Claude
into his workflow across feature planning, code generation, and service layer scaffolding.

Ionic framework and mobile dashboard design: Covered feature-based component structure, ion-grid
responsiveness, virtual scroll for large datasets, and lazy loading modules.

Capacitor plugins: Explained using Camera, Filesystem, and Network plugins; walked through the
conceptual flow of capturing an image, converting to base64, and syncing on connectivity change.

Live coding (Capacitor): Attempted a JavaScript snippet for camera capture and filesystem write;
structure was partially correct but execution was incomplete and required prompting.

Tailwind CSS: Described utility-first approach, @apply for reusable patterns, and a workflow of
aligning global color tokens with stakeholders before development begins.

Angular modular architecture: Outlined separation of Core, Shared, and Feature modules with lazy
loading; referenced RxJS and NgRx for state management at different complexity levels.

React state management: Described splitting state into global, server, and local layers using
Context API and React Query; unfamiliar with Zustand in practice despite writing a rough outline
when prompted.

CANDIDATE PROFILE
Frontend/Mobile Engineer, mid-level. Prasanna has 9 years of experience with a strong focus on
Angular, React, Ionic, and Capacitor. His breadth across the stack is genuine: he could describe
architectural patterns, plugin integrations, and AI tool usage with reasonable fluency. The
concern is depth under pressure: his live coding answers were hesitant and incomplete, and he
acknowledged not having used Zustand. His verbal explanations were sometimes fragmented, which
may become an issue in cross-functional or client-facing settings.

CANDIDATE SUMMARY
Prasanna Kumar is a 9-year frontend and mobile developer with a solid foundation in Angular,
React, and Ionic-based hybrid mobile applications. His strongest areas are architectural
thinking (modular Angular structures, feature-based Ionic layouts, Capacitor plugin integration)
and practical AI tool adoption, having used Cursor, Copilot, and Claude as part of daily
development for two years. He is weakest under live coding conditions where he either produced
incomplete snippets or was unsure of libraries he had not directly used (notably Zustand). His
communication is functional but not polished, with answers that sometimes needed follow-up
prompting to reach a concrete point. He is a reasonable candidate for mid-level frontend or
hybrid mobile roles where architectural guidance is provided and independent live problem-solving
is not a primary requirement.
```

### Output (Transcript 2)

```
TOPICS COVERED
End-to-end process ownership (fraud detection): Candidate described building a fraud risk
scoring system from scratch, integrating Experian, CIBIL, Truecaller, and telecom APIs,
enrolling banking partners, and reducing audit load by roughly 90%.

Vendor management: Covered sourcing, onboarding, performance monitoring, and a structured
offboarding process involving hierarchy escalation, contract review, and gradual volume reduction.

Cross-functional project delivery: Described managing three misaligned departments with phased
milestone tracking and bi-weekly check-ins while maintaining healthy skepticism of self-reported
timelines.

BPO and calling operations: Explained upgrading from manual calling to predictive dialing, CRM
pop-ups, and call routing to reduce idle time and improve counselor efficiency.

KPI tracking and executive reporting: Described weekly and monthly business reviews covering
revenue, refunds, ROAS, CAC, and team-level performance breakdowns.

Stakeholder prioritization and conflict handling: Walked through a framework for ranking P1
requests from competing stakeholders, including how to communicate deprioritization without
losing trust.

Data credibility under pressure: Described how he handled a major internal scam case by
gathering irrefutable analytics data to overcome VP-level resistance.

CANDIDATE PROFILE
Operations Program Manager, mid-senior. Krishna has approximately 6 years of experience across
ed-tech operations, fraud prevention, and business analytics, with demonstrated ownership of
multi-stakeholder, cross-functional initiatives. His answers showed real depth: he cited specific
integrations, vendor names, risk scoring logic, and KPI frameworks rather than speaking in
generalities. He thinks in structured decision trees (for vendor management, stakeholder
prioritization, and data disputes). The one flag the interviewer raised, and which the transcript
confirms, is a tendency to mix Hindi idioms and jargon under pressure, which may create friction
in senior leadership or international settings.

CANDIDATE SUMMARY
Krishna brings roughly 6 years of operations and program management experience, primarily in
ed-tech, with a track record of building systems and processes from scratch rather than
inheriting them. His clearest strengths are analytical rigour (the fraud scoring model and data
investigation case are both well-evidenced examples), vendor lifecycle management, and the
ability to navigate upward with data when facing resistance. His communication in English is
clear and structured in most parts of the interview, but the interviewer's feedback about Hindi
jargon is consistent with some moments in the transcript where explanations became idiomatic
rather than precise. He has not operated at the level of large enterprise multi-region programs,
and the scope of his work, while impressive in an early-stage or startup context, may require
calibration for a larger organizational environment. Overall, a strong candidate for a mid-senior
operations or program management role in a fast-moving company that values process ownership and
data-driven decision making.
```

### What Worked / What Did Not

The role classification finally corrected on Transcript 1 to "Frontend Engineer" because the 3-to-5 sentence justification requirement forced the model to engage with what the interview actually covered rather than the resume stack. The system prompt eliminated most of the filler language across both transcripts, and adding explicit non-technical evaluation criteria gave Transcript 2 a real framework instead of vague operational praise. The one thing still not fully resolved is the Transcript 1 summary slipping in "making them a promising candidate" at the end, exactly the kind of generic closer the system prompt was supposed to block. A concrete negative example in the system prompt showing what a weak closing looks like versus a strong one would be the next fix.
