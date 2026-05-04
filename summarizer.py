# Install Groq SDK (run once)
!pip install -q groq

import os
from groq import Groq
from getpass import getpass


# 🔐 Enter API key securely
os.environ["GROQ_API_KEY"] = getpass("Enter your Groq API key: ")


# ------------------ SYSTEM PROMPT ------------------ #

SYSTEM_PROMPT = """You are a senior technical recruiter and talent analyst with 15 years of experience evaluating
candidates across engineering, product, and operations roles. You read interview transcripts
carefully and produce structured, honest, and useful summaries for hiring teams.

Your summaries must be grounded strictly in what the transcript shows. Do not invent or assume
skills or experiences not evidenced in the conversation. If the transcript is short or vague on
a dimension, say so honestly rather than filling gaps with generic praise.

You write in clear, direct English. No filler phrases like "the candidate demonstrated a strong
passion for" or "showcases exceptional talent." Be specific. Reference actual moments from the
transcript when relevant.
"""


# ------------------ USER PROMPT ------------------ #

USER_PROMPT_TEMPLATE = """Read the following interview transcript carefully, then produce a structured candidate summary
with exactly three sections.

--- TRANSCRIPT START ---
{transcript}
--- TRANSCRIPT END ---

Now write the structured summary using this exact format. Do not add extra sections or change the
section headers.

TOPICS COVERED
List the main themes and subject areas discussed in this interview. For each topic, write one line:
the topic name followed by a colon and a brief note on what was actually covered. Aim for 4 to 8
topics. Focus on what was substantively discussed, not just briefly mentioned.

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
"""


def generate_summary(transcript):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(transcript=transcript)}
        ],
        temperature=0.3,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()



transcript = """
[12:37] Interviewer: My name is Pranav and I have 14 plus years of experience. My expertise are mobile app development, CSS frameworks, Angular, React and AI system software development.
[13:06] Candidate: Hi sir. My name is Prasanna Kumar. I have around nine plus years of experience in software development. My core technical expertise is on Angular, React and Ionic framework. I'm working with the backend by using Node.js, Express and .NET Core.
[13:33] Candidate: I've worked mostly on service-based applications, risk assessment management tools, and communication-based applications. Mainly I focus on Ionic Angular and Ionic Capacitor and Cordova for native functionalities and I deployed applications to iOS and Android. AI assist — Cursor, GitHub Copilot and Claude for the last two years.
[14:28] Interviewer: This interview will be focused on AI-assisted software development, mobile app development, CSS framework, Angular, React, communication and articulation.
[15:11] Interviewer: First topic — AI powered coding assistance. You are building a complex feature involving form validation, API integration and state synchronization across multiple components. Show how you would practically use an AI coding assistant throughout the development life cycle.
[20:01] Candidate: First, I will be understanding the requirements. Stakeholder thoughts, which platforms. Then architecture level — mobile platforms, hybrid development, API design. And team building — who has Ionic experience, who has Angular.
[20:57] Candidate: Generate the initial model and component structure. The prompt: "generate a React form with the fields of name, email, phone with validations" with proper error messaging.
[21:46] Candidate: For Ionic: "generate the application with Ionic 7 with Angular, validations and proper architecture, like a folder structure". Along with that I wanted to give Capacitor.
[22:29] Candidate: For service-based applications, mostly forms and check boxes — I will be creating reusable UI components firstly.
[23:58] Candidate: Then API integration. If I have the chance to work on the backend, I will be developing parallelly, frontend and backend.
[24:57] Candidate: Service layer: "create an Angular service with the CRUD operations using HTTP client and retry and error handling". If I wanted to add anything manually, like interceptors or centralized error handling and strong typing, I will be adding manually.
[25:26] Candidate: State management — "create the shared state between the components using the RxJS BehaviorSubject".
[26:26] Candidate: I will be integrating AI into my IDE — Cursor or any codex. From there I will be starting the scratch onwards.
[27:13] Interviewer: Next topic — Ionic Framework. You are building a mobile first dashboard using Ionic v7 plus that must work seamlessly across devices. How would you structure the UI, handle responsiveness and ensure performance for large datasets?
[27:41] Candidate: Feature based reusable components. Feature modules like dashboard, reports, settings. Reusable components like cards, data table list, filters and loaders for lazy loading.
[28:39] Candidate: Responsive — Ionic grid plus CSS. Ion grid, ion row, ion columns. Commands — NPM install Ionic CLI, Ionic run, Ionic build.
[29:22] Candidate: Layout — flexbox grid and media queries. I wanted to avoid some width because flexbox or grid will be adjusting based on screen resolution.
[29:53] Candidate: Large data sets — virtual scroll, pagination, lazy loading.
[30:21] Candidate: Performance — lazy loading modules. For loops, trackBy. Search, debouncing. Service layer with retry error handling.
[30:52] Candidate: Mobile optimization — reduce bundle size, optimizing images, avoiding unnecessary plugins. Testing — emulators or mobile devices.
[31:46] Interviewer: Next — Capacitor and plugin ecosystem. You need to capture images, store them locally and sync to a back-end when online. Design how you would use Capacitor and plugins. Implement a small snippet around how would you get the photo and write the file to the file system.
[32:33] Candidate: I will be using plugins. Capacitor is for native functionalities. Capacitor camera. And file system, for storing. And Capacitor plugin like network.
[33:59] Candidate: Once captured the image by camera plugin, then converting that into base 64. Then save into file system layer by using the file system. Then storing — either in DB or local storage. Once it is listen for network changes, syncing pending files to the backend.
[36:39] Interviewer: If you could write a JavaScript code for getting the photo from the camera and writing to the file system.
[36:51] Candidate: Okay. I will be writing some structure. Capture image. I wanted to maintain quality and result. Camera result. Camera source I will be declaring. Then it will be returning that image.
[38:37] Candidate: Then store into local storage. Sorry, here I wanted to write — I think because I'm using here I wait. Here it is totally related to promises. For example save image. Here I will be using the await.
[39:30] Candidate: We have the file system plugin. And camera plugin. Just I am writing main logic, all the declarations will be included into import sections.
[40:27] Interviewer: Next topic — CSS framework utility classes. You need to build a highly responsive design system across web and mobile using Tailwind. How would you structure your styling approach for scalability?
[40:54] Candidate: First I wanted to require Tailwind config. For light or dark related thing, by using Tailwind config it will be implementing globally.
[41:19] Candidate: Utility-first approach — by using of repeated pattern into reusable component by using of @apply.
[41:49] Candidate: Mobile-first responsive — we have breakpoints. Reusable UI components — buttons, cards, inputs, check boxes.
[42:52] Candidate: Before starting the application, I will be approaching for styles and main color patterns from stakeholders. Based on that, I will be creating global styles as a centralized layer.
[43:20] Candidate: Concentrating on reusable components and reusable styles globally.
[44:08] Interviewer: Next topic — Angular Framework. Design a scalable Angular application structure for a large enterprise dashboard with multiple modules, shared components and complex data flow.
[44:59] Candidate: Modular architecture. Core principles — separation of folders, lazy loading for scalability, reusable shared components. Data flow between state management.
[45:26] Candidate: For source — separation. Core — services, data services, guards. Shared components — components, directives, pipes.
[47:37] Candidate: For dashboard — separating each component level. Pages — login covers sign up. Dashboard.
[49:07] Candidate: Core module — services and API error handlings like HTTP interceptors. Shared modules — pipes, UI components, date pipes.
[49:46] Candidate: State management — RxJS for simple cases, NgRx for the data flow. Clean service layer for API integrations. Singleton services like authentication and interceptors and shared UI dependencies.
[50:57] Interviewer: Next topic — state management in React. You are building a large scale React application with multiple shared states — user session, UI preferences, API data caching. How would you design the state management strategy?
[53:51] Candidate: Splitting state. Global state — session, users token, theme preferences. Server state — data from back end, caching and re-fetching. Local UI state — component level, forms and modals.
[54:21] Candidate: For global state, Context API along with reducer for token management. For server state, React Query.
[55:01] Interviewer: Have you used Zustand?
[55:05] Candidate: Zustand, I cannot use this. I worked on React Query.
[55:14] Interviewer: Can you write an example of Zustand for creating a useStore?
[55:24] Candidate: Yeah. Like a constant. Use store. This is the base structure.
[56:23] Interviewer: Can you also write the code for redux slice?
[56:30] Candidate: Redux slice, okay. I will write.
[57:21] Interviewer: You need to create a user slice.
[57:25] Candidate: I wanted to create a user slice. I will be declaring interface.
[58:54] Candidate: ID as string. Interfaces for basic details, this is also string. Then email.
[59:32] Interviewer: That's fine. Let's not waste time. Let's create TypeScript code for redux slice only.
[1:00:16] Interviewer: Do you know what is createSlice method in Redux slice?
[1:00:19] Candidate: Yes, sir. We will be using for reducing function for specific related things. We needed to write inside that slice for state changes.
[1:00:56] Interviewer: Understood. We have covered all the topics. Thanks for joining.
[1:01:04] Candidate: Okay, fine. Thanks. Bye.
"""



def pretty_print(text):
    print("\n" + "=" * 60)
    print("INTERVIEW SUMMARY")
    print("=" * 60 + "\n")

    # Fix line breaks properly
    print(text.replace("\\n", "\n"))

    print("\n" + "=" * 60)



print("Generating summary...\n")
summary = generate_summary(transcript)
pretty_print(summary)
