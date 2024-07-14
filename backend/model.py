from llama_cpp import Llama
from transformers import pipeline


def relabel(mapping):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            results = f(*args, **kwargs)
            for result in results:
                for obj in result:
                    obj["label"] = mapping.get(obj["label"], obj["label"])
            return results
        return wrapped
    return wrapper


class LLM:
    def __init__(self):
        # https://huggingface.co/Qwen/Qwen2-0.5B-Instruct-GGUF
        # limited to small model since running on CPU, Qwen2-7B will have 128k context tokens
        self.model = Llama.from_pretrained(
            repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
            filename="qwen2-0_5b-instruct-q4_k_m.gguf",
            verbose=False
        )

    def __call__(self, *args, **kwargs):
        raw_output = self.model.create_chat_completion(*args, **kwargs)
        return raw_output["choices"][0]["message"]["content"]


class TfModel:
    def __init__(self, model):
        self.model = model

    def __call__(self, *args, **kwargs):
        raw_output = self.model(*args, **kwargs)
        return {ele["label"]: ele["score"] for ele in raw_output[0]}


class EmotionClassifier(TfModel):
    def __init__(self):
        # https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion
        model = pipeline(
            model='bhadresh-savani/distilbert-base-uncased-emotion',
            task='text-classification',
            top_k=None,
        )
        super().__init__(model)


class OffensiveDetector(TfModel):
    def __init__(self):
        # https://huggingface.co/cardiffnlp/twitter-roberta-base-offensive
        model = pipeline(
            model='cardiffnlp/twitter-roberta-base-offensive',
            top_k=None,
        )
        super().__init__(model)


class QuestionDetector(TfModel):
    def __init__(self):
        # https://huggingface.co/shahrukhx01/question-vs-statement-classifier
        model = relabel({
            "LABEL_0": "statement",
            "LABEL_1": "question",
        })(
            pipeline(
                model='shahrukhx01/question-vs-statement-classifier',
                tokenizer='shahrukhx01/question-vs-statement-classifier',
                top_k=None,
            )
        )
        super().__init__(model)


class MentalHealthClassifier(TfModel):
    def __init__(self):
        # https://huggingface.co/facebook/bart-large-mnli
        model = pipeline(
            model='facebook/bart-large-mnli',
            top_k=None,
            task="zero-shot-classification",
        )
        super().__init__(model)

    def __call__(self, *args, **kwargs):
        raw_output = self.model(
            *args, ['bad mental state', 'neutral mental state', 'good mental state'])
        return dict(zip(raw_output["labels"], raw_output["scores"]))


model_llm = LLM()
model_emotion_classifier = EmotionClassifier()
model_offensive_detector = OffensiveDetector()
model_question_detector = QuestionDetector()
model_mental_health_classifier = MentalHealthClassifier()


def get_seed(topic):
    return model_llm([
        {
            "role": "system",
            "content": f"You are a patient teacher, who is going to speak to your grade-school student about some specific subtopic (you decide) in {topic}. Start this conversation by explaining the subtopic to the student as if you were starting a class. Generate at most 2 paragraphs in a conversational prose to start a conversation."
        }
    ])


def get_completion(topic, seed, message):
    return model_llm([
        {
            "role": "system",
            "content": f"You are a patient teacher who is teaching your student about a sub-topic in {topic}. Keep replies short and professionally to-the-point as in instant-message (IM) style."
        },
        {
            "role": "assistant",
            "content": seed
        },
        {
            "role": "user",
            "content": message
        }
    ])


def get_majority(output):
    return max(output, key=output.get)


def analyze(message):
    emotion_output = model_emotion_classifier(message)
    offensive_output = model_offensive_detector(message)
    question_output = model_question_detector(message)
    mental_health_output = model_mental_health_classifier(message)

    major_emotion = get_majority(emotion_output)
    major_offensive = get_majority(offensive_output)
    major_question = get_majority(question_output)
    major_mental_health = get_majority(mental_health_output)

    is_offensive = major_offensive == "offensive"
    is_bad_mental_state = major_mental_health == "bad mental state" and mental_health_output[
        major_mental_health] >= 0.9
    should_reply = not is_offensive and not is_bad_mental_state

    return {
        "sentiments": [{"sentiment": "emotion",
                       "major": major_emotion,
                        "score": emotion_output[major_emotion]
                        },
                       {"sentiment": "offensive",
                        "major": major_offensive,
                        "score": offensive_output[major_offensive]
                        },
                       {"sentiment": "question",
                        "major": major_question,
                        "score": question_output[major_question]
                        },
                       {"sentiment": "mental_health",
                        "major": major_mental_health,
                        "score": mental_health_output[major_mental_health]
                        }],
        "should_reply": should_reply,
    }
