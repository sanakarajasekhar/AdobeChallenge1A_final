# Adobe India Hackathon - Challenge 1A

We use `pdfplumber` to parse each PDF and extract:
- Title: First large text on top 20% of page 1
- Headings: H1–H3 assigned based on relative font sizes

```bash
docker build --platform linux/amd64 -t adobe-heading-extractor:v1 .

#this is used to run the docker file use this command

docker run --rm `
  -v "${PWD}\sample_datasets\pdfs:/app/sample_datasets/pdfs" `
  -v "${PWD}\sample_datasets\outputs:/app/sample_datasets/outputs" `
  heading-extractor

