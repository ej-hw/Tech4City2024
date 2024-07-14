# Judy: A chatbot who knows when to shut up.

> Submitted by team **Cikgang** for the Entry Coding Challenge of the Huawei Tech4City 2024 Competition Semi-finals.

The problem with most teaching chatbots is they usurp the learning experience and keeps replying. This is a proof-of-concept of a chatbot with analysis features to determine when it should stop replying and fall back to a human.

Our project, Cikgo, will eventually develop a feature called Autoreply, which automatically generates replies to messages sent by students. To be useful, Autoreply's engine must be able to determine _when to stop replying and fall back to a human_. For example,

1. if a student repeatedly returns with more questions, i.e., the AI-generated replies aren't helping,
2. if a student's message indicates a bad mental state, e.g., depression (not necessarily clinical), suicidal indications, etc.,
3. if a student digresses from the topic of the conversation, e.g., personal issues, other unrelated topics, etc., or
4. anything else that isn't ethically or productively answerable by AI, or is best answered by human teachers.

> [!NOTE]
> For this proof-of-concept, we use open-source NLP models that run locally. Analysis results may not be accurate. However, analyses' quality can be improved with better models and/or heuristics. In this project, this aspect is left as an abstraction. We selected the best NLP models we could find and focused on building a minimum viable product.

# Usage Instructions

```sh
docker build -t judy .
docker run -it --rm -v ./hub:/app/hub -p 8080:8080 judy
```
