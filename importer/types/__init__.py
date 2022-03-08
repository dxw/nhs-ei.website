def trim_long_text(text, length):
    if len(text) > length:
        return text[0:length]
    return text
