import pysrt

def load_srt(input_srt_path):
    subs = pysrt.open(input_srt_path, encoding="utf-8")

    result = []

    for sub in subs:
        srt_content = {"index": sub.index,
                       "start": sub.start,
                       "end": sub.end,
                       "text": sub.text}
        result.append(srt_content)

    return result
