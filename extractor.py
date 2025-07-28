import fitz  # PyMuPDF
import re
import json
from collections import Counter
import os

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def is_heading(text):
    text = clean(text)
    return len(text) >= 10 and sum(c.isalnum() for c in text) / len(text) > 0.6

def merge_multilines(lines, y_thresh=5, x_thresh=10):
    merged, buf = [], []
    for line in lines:
        if not buf:
            buf.append(line)
            continue
        last = buf[-1]
        if abs(line['y0'] - last['y1']) < y_thresh and abs(line['x0'] - last['x0']) < x_thresh:
            buf.append(line)
        else:
            text = " ".join(l['text'] for l in buf)
            merged.append({'text': clean(text), 'size': buf[0]['size'], 'page': buf[0]['page']})
            buf = [line]
    if buf:
        text = " ".join(l['text'] for l in buf)
        merged.append({'text': clean(text), 'size': buf[0]['size'], 'page': buf[0]['page']})
    return merged

def extract_title(doc):
    spans = sorted(
        [s for b in doc[0].get_text("dict")["blocks"] if "lines" in b
         for l in b["lines"]
         for s in l["spans"]],
        key=lambda s: (-s["size"], s["bbox"][1])
    )
    for s in spans:
        text = clean(s["text"])
        if len(text.split()) > 4:
            return text
    return "Untitled Document"

def extract_headings(doc):
    raw = []
    for page in doc:
        pnum = page.number + 1
        for block in page.get_text("dict")["blocks"]:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = " ".join(clean(s["text"]) for s in spans)
                if not is_heading(text): continue
                x0 = min(s["bbox"][0] for s in spans)
                y0 = min(s["bbox"][1] for s in spans)
                y1 = max(s["bbox"][3] for s in spans)
                size = max(s["size"] for s in spans)
                raw.append({'text': text, 'size': round(size, 1), 'page': pnum, 'x0': x0, 'y0': y0, 'y1': y1})
    merged = merge_multilines(raw)
    levels = {s: f"H{i+1}" for i, (s, _) in enumerate(Counter(x['size'] for x in merged).most_common(3))}
    seen, structured = set(), []
    for m in merged:
        k = (m['text'], m['page'])
        if k not in seen and m['size'] in levels:
            seen.add(k)
            structured.append({'level': levels[m['size']], 'text': m['text'], 'page': m['page']})
    return structured

def process(pdf_path):
    doc = fitz.open(pdf_path)
    result = {
        "title": extract_title(doc),
        "outline": extract_headings(doc)
    }
    doc.close()
    return result

if __name__ == "__main__":
    in_dir, out_dir = "./input", "./output"
    os.makedirs(out_dir, exist_ok=True)
    for file in os.listdir(in_dir):
        if not file.endswith(".pdf"):
            continue
        path = os.path.join(in_dir, file)
        try:
            result = process(path)
            outpath = os.path.join(out_dir, file.replace(".pdf", ".json"))
            with open(outpath, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2)
            print(f"[✓] Processed: {file}")
        except Exception as e:
            print(f"[✗] Failed: {file} — {e}")
