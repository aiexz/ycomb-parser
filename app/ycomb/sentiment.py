from typing import Any

np: Any
softmax: Any


class TextClassifier:
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer: Any
    config: Any
    model: Any

    @staticmethod
    def load_model():
        global np, softmax
        import numpy as np  # type: ignore
        from scipy.special import softmax  # type: ignore
        from transformers import AutoModelForSequenceClassification
        from transformers import AutoTokenizer, AutoConfig
        TextClassifier.tokenizer = AutoTokenizer.from_pretrained(TextClassifier.MODEL)
        TextClassifier.config = AutoConfig.from_pretrained(TextClassifier.MODEL)
        TextClassifier.model = AutoModelForSequenceClassification.from_pretrained(TextClassifier.MODEL)

    @staticmethod
    def classify_sentiment(text) -> dict:
        if hasattr(TextClassifier, "model") is False:
            return {"neutral": 1.0}
        output = TextClassifier.model(**TextClassifier.tokenizer(text, return_tensors='pt'))
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)
        ranking = ranking[::-1]  # now in descending order
        return {TextClassifier.config.id2label[ranking[i]]: np.round(float(scores[ranking[i]]), 4) for i in
                range(scores.shape[0])}
