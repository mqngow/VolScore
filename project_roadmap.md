# Sheet Music Analyzer & Recommender Roadmap

This document outlines a phased approach to building your sheet music scoring and recommendation app. The grand vision is ambitious, so the best way to tackle it is by starting with the easiest data formats and progressively adding complexity.

## Technology Stack Recommendations

Before diving into the roadmap, here are the best tools available for reading and analyzing music data, which will be the core of your application.

### 1. Data Ingestion (Reading the Music)
*   **For MIDI and MusicXML (Highly Recommended):**
    *   **[`music21`](http://web.mit.edu/music21/) (Python):** This is the gold standard for computational musicology. It can read MIDI, MusicXML, and many other formats. It actually understands musical concepts (measures, time signatures, chords, hands), which makes it perfect for your use case.
    *   **[`pretty_midi`](https://github.com/craffel/pretty-midi) (Python):** If you only deal with MIDI, this library is fantastic for easily extracting raw note data (pitch, start time, end time, velocity).
*   **For PDF / Sheet Music Scans (OMR - Optical Music Recognition):**
    *   *Note: Extracting data from PDFs is notoriously difficult and error-prone. It is highly recommended to save this for later.*
    *   **[Audiveris](https://github.com/Audiveris/audiveris) (Java):** The most mature open-source OMR engine. You can run it via command line to convert PDFs into MusicXML, which your Python app can then read using `music21`.
    *   **[Oemer](https://github.com/BreezeWhite/oemer) (Python):** A modern, machine-learning-based OMR system that attempts to do end-to-end sheet music transcription to MusicXML.

### 2. Backend & Database
*   **Language:** Python (due to the overwhelming superiority of its data analysis and music libraries).
*   **Database:** PostgreSQL or SQLite. You will need to store structured data (songs, their metadata, and their 5-6 different attribute scores).
*   **Framework:** FastAPI or Flask for serving the backend to your frontend.

---

## Development Roadmap

### Phase 1: Foundation (Data Ingestion & Parsing)
**Goal:** Get a program to successfully read a song file and output a list of notes and timings.
*   **Focus on MIDI or MusicXML first.** Do not start with PDFs. Sites like MuseScore allow you to download `.mscz` files (which are just zipped MusicXML) or standard MIDI files.
*   **Task:** Write a Python script using `music21` that loads a MIDI/MusicXML file and iterates through all the notes, printing their pitch, duration, and which hand (or track) they belong to.

### Phase 2: Feature Extraction (The Core Logic)
**Goal:** Translate raw note data into your specific "difficulty attributes".
*   **Task:** Write algorithms to calculate your metrics over the course of the song.
    *   *Note Density:* Count notes per measure or notes per second.
    *   *Spread/Reach:* Calculate the maximum interval (distance) between the highest and lowest note played simultaneously by one hand.
    *   *Speed:* Find the shortest note durations or fastest consecutive note sequences.
    *   *Hand Independence/(One hand):* Analyze how often rhythms in the left and right hands conflict (polyrhythms or syncopation).
    *   *Leaps:* Calculate the average and maximum distance (in semitones) between consecutive notes.
    *   *Complexity/(Tricky):* Frequent time signature changes, complex subdivisions such as triplets, quintuplets, etc.
*   **Task:** Output a JSON object or dictionary with the raw numerical values for a specific song.

### Phase 3: The Scoring System
**Goal:** Normalize the raw data into a human-readable 1-100 or 1-10 scale.
*   **Task:** Determine the baseline. You will need to feed your Phase 2 script a very easy song (e.g., "Twinkle Twinkle Little Star") and a wildly difficult song (e.g., "La Campanella") to establish the minimum and maximum bounds for your scores.
*   **Task:** Create an algorithm that combines the separate attribute scores into one **Total Difficulty Score**.

### Phase 4: Database & User Tracking
**Goal:** Save the analysis and allow a user to track their progress.
*   **Task:** Set up a database. Create a `Songs` table (with columns for overall score, speed score, spread score, etc.) and a `Users` table.
*   **Task:** Create a system where a user can mark a song as "Played" or "Mastered".
*   **Task:** Calculate a user's current "Skill Profile" (e.g., their average speed score is 45, but their spread score is 70).

### Phase 5: The Recommendation Engine
**Goal:** Suggest songs based on the user's weaknesses.
*   **Task:** Write a query that finds the user's lowest-scoring attribute (their weak area).
*   **Task:** Search the database for songs that have a slightly higher score in that specific attribute than the user's current average, while keeping the *overall* difficulty within their grasp. (e.g., "Here is a song that is easy overall, but specifically challenges your note-reach").

### Phase 6: Web Interface & UI
**Goal:** Make it usable for non-programmers.
*   **Task:** Build a frontend (React, Next.js, or even a quick Streamlit app in Python).
*   **Task:** Allow users to upload a MIDI file through the browser, have the backend score it instantly, and display the results in a radar chart or graph.

### Phase 7: PDF Integration (The Final Boss)
**Goal:** Accept PDF sheet music.
*   **Task:** Integrate an OMR pipeline (like Audiveris).
*   **Task:** When a user uploads a PDF, route it through the OMR to generate a temporary MusicXML file, and then feed that XML file into your Phase 1 pipeline. You will need to handle errors gracefully here, as OMR is rarely 100% accurate.