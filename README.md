# Adobe India Hackathon - Challenge 1A

We use `pdfplumber` to parse each PDF and extract:
- Title: First large text on top 20% of page 1
- Headings: H1–H3 assigned based on relative font sizes

```bash
docker build --platform linux/amd64 -t adobe-heading-extractor:v1 .
