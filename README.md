# Website Cloning with LLMs

This project automates the process of statically cloning the visual and structural layout of any public website using large language models. It combines web scraping, screenshot analysis, and prompt-driven code generation, wrapped in a full-stack application powered by FastAPI and Next.js.

## 🧠 Key Features

- **Playwright Automation**: Captures both the DOM structure and full-page screenshots of target websites.
- **Prompt Engineering**: Uses LLMs to analyze extracted content and generate clean, semantic HTML/CSS to match the original layout.
- **Full-Stack Architecture**: Integrates a React-based Next.js frontend with a FastAPI backend to manage scraping, prompt handling, and result delivery.
- **Static Cloning**: Outputs static site clones that preserve visual fidelity and layout hierarchy without JavaScript functionality.

## 🛠 Tech Stack

- **Frontend**: Next.js
- **Backend**: FastAPI (Python)
- **Web Scraping**: Playwright
- **LLMs Used**: OpenAI GPT, Gemini (pluggable support via prompt endpoints)
- **Tooling**: Python, JavaScript

## 🚀 How It Works

1. **Input**: User enters the URL of a public website.
2. **Scraping**: Playwright loads the page, captures the DOM and a screenshot.
3. **Code Generation**: A backend prompt is sent to an LLM with the extracted HTML, CSS context, and visual hints.
4. **Output**: The LLM returns a clean, static HTML/CSS clone that replicates the look and structure of the site.
5. **Delivery**: The result is displayed in the frontend and available for download/export.

## 💡 Example Prompt

> "Here is the DOM and a screenshot of a website. Recreate this layout as static HTML and CSS. Do not use JavaScript."

The LLM is instructed to:
- Maintain responsive structure
- Replicate font, spacing, and visual hierarchy
- Avoid interactive elements like forms or modals


## 📌 Limitations

- Focuses on visual and structural replication only — dynamic JavaScript functionality is not cloned.
- Performance may vary depending on the complexity of the original site and the LLM used.
