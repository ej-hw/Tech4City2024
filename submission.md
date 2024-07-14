# Judy: A chatbot who knows when to shut up.

> Submitted by team **Cikgang** for the Entry Coding Challenge of the Huawei Tech4City 2024 Competition Semi-finals.

The problem with most teaching chatbots is they usurp the learning experience and keeps replying. This is a proof-of-concept of a chatbot with analysis features to determine when it should stop replying and fall back to a human.

> [!NOTE]
> The chatbot is called Judy, derived from the word "judicious", meaning _having, showing, or done with good judgement or sense_. We chose this word because the chatbot is designed to make judicious decisions on when to stop replying.

Our project, Cikgo, will eventually develop a feature called Autoreply, which automatically generates replies to messages sent by students. To be useful, Autoreply's engine must be able to determine _when to stop replying and fall back to a human_. For example,

1. if a student repeatedly returns with more questions, i.e., the AI-generated replies aren't helping,
2. if a student's message indicates a bad mental state, e.g., depression (not necessarily clinical), suicidal indications, etc.,
3. if a student digresses from the topic of the conversation, e.g., personal issues, other unrelated topics, etc., or
4. anything else that isn't ethically or productively answerable by AI, or is best answered by human teachers.

> [!NOTE]
> For this proof-of-concept, we use open-source NLP models that run locally. Analysis results may not be accurate. However, analyses' quality can be improved with better models and/or heuristics. In this project, this aspect is left as an abstraction. We selected the best NLP models we could find and focused on building a minimum viable product.

## Usage

### Building the Docker image

Run this command in the root directory of this repository.

```sh
docker build -t judy .
```

### Starting the Docker container

After the above command builds `judy:latest`, you can run the Docker container to start Judy.

```sh
docker run -it --rm -v ./hub:/app/hub -v ./data:/app/data -p 8000:8000 judy
```

This command will mount two volumes,

- `/hub` for storing models downloaded from [Hugging Face](https://huggingface.co/), so that the models need not be redownloaded across container restarts, and

- `/data` for storing `database.db`, so that the database is persisted across container restarts.

> [!NOTE]
> When you first start Judy, you may need to wait while all the models are being downloaded. Subsequent starts will be much faster as all the models will be cached in `/hub`.

### Accessing the web application

Go to `http://localhost:8000` in your browser to access the web application.

> [!WARNING]
> Due to the challenge constraints of needing to use only vanilla JavaScript, there are no polyfills or additional build processes added to increase compatibility of the web application across different browsers and operating systems. It is highly recommended to access the Judy with the latest version of Google Chrome.

## Architecture

### The front-end

The front-end is built using HTML, CSS, and vanilla JavaScript. As allowed by the committee, styling is powered by [Tailwind CSS](https://tailwindcss.com/). Icons are retrieved from [Lucide](https://lucide.dev/).

We heavily rely on [the `<template>` element](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/template) for templating and rendering.

### The back-end

The REST web server is powered by [Flask](https://flask.palletsprojects.com/en/3.0.x/). The API documentation is available at `http://localhost:8000/api/docs` and is powered by [Swagger](https://swagger.io/).

The database is powered by [SQLite](https://www.sqlite.org/). The web server uses [SQLAlchemy](https://www.sqlalchemy.org/) as the object relational mapper (ORM) layer.

> [!NOTE]
> No `database.db` was committed to the repository. The web server will create it if it doesn't exist when it first starts. The schema is available in `backend/database.py`.

### The AI models

The AI models we use are retrieved from [Transformers in Hugging Face](https://huggingface.co/docs/transformers/en/index). In particular, we use the following models.

| Model                                                                                                                     | Usage                                         | Notes                                                                                                                                                                        |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Qwen/Qwen2-0.5B-Instruct-GGUF](https://huggingface.co/Qwen/Qwen2-0.5B-Instruct-GGUF)                                     | Natural language understanding and generation | Used to generate conversational starters as well as contextually relevant replies. We chose this model to balance performance and resource consumption (no GPU environment). |
| [bhadresh-savani/distilbert-base-uncased-emotion](https://huggingface.co/bhadresh-savani/distilbert-base-uncased-emotion) | Emotion detection                             | Employs the DistilBERT model fine-tuned for emotion detection to understand the emotional context of the conversation.                                                       |
| [cardiffnlp/twitter-roberta-base-offensive](https://huggingface.co/cardiffnlp/twitter-roberta-base-offensive)             | Offensive content filtering                   | Uses the RoBERTa model fine-tuned for offensive content detection to ensure the conversation remains appropriate.                                                            |
| [shahrukhx01/question-vs-statement-classifier](https://huggingface.co/shahrukhx01/question-vs-statement-classifier)       | Question detection                            | Integrates a BERT-mini model fine-tuned for question detection to distinguish if the user is asking a question or making a statement.                                        |
| [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli)                                               | Mental state classification                   | Leverages the BART model for zero-shot classification to understand the mental state of the user.                                                                            |

## About the interface

The interface is split into 3 left-to-right sections: Chat Interface, Analysis Results, and History.

![Full Interface](images/interface.png)

### The chat interface

Provides a simple chat interface for users to interact with the chatbot. You can directly start typing a message, or choose to generate a conversational starter first.

<img src="images/chat.png" alt="Chat" title="Chat" height="300"/>

### Analysis results

Displays the results of the AI/ML sentiment analyses used to analyse the message. This section also flags out if the chatbot is unable to provide appropriate responses, and human intervention is required.

<img src="images/analysis.png" alt="Analysis" title="Analysis" height="300"/> <img src="images/human.png" alt="Human Intervention" title="Human Intervention" height="300"/>

### History

Shows all past messages and analyses of the conversation. You can restore any previous analyses or delete the message permanently here.

<img src="images/history.png" alt="History" title="History" height="300"/>
