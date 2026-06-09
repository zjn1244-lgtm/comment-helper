from config.keywords import COMMENT_KEYWORDS


DEFAULT_TAG = "普通评论"


def classify_comment(content):
    if content is None:
        return DEFAULT_TAG

    comment_text = str(content)

    for tag in ["风险评论", "高价值评论", "值得回复评论"]:
        for keyword in COMMENT_KEYWORDS[tag]:
            if keyword in comment_text:
                return tag

    return DEFAULT_TAG
