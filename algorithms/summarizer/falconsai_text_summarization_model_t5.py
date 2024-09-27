def summarize_model_t5(text):
    from transformers import pipeline

    summarizer = pipeline("summarization", model="Falconsai/text_summarization")
    summary = summarizer(text, max_length=300, min_length=3)

    return summary