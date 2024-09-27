from transformers import pipeline


def summarize(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=300, do_sample=False)

    return summary
