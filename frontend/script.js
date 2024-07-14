const historyItemTemplate = document.getElementById("history-item-template");
const botOffIconTemplate = document.getElementById("bot-off-icon");
const sentimentTemplate = document.getElementById("sentiment-template");
const fallbackTemplate = document.getElementById("fallback-template");
const responseTemplate = document.getElementById("response-template");
const loaderTemplate = document.getElementById("loader-template");
const errorDialogTemplate = document.getElementById("error-dialog-template");
const seedTemplate = document.getElementById("seed-template");
const emptyHistoryTemplate = document.getElementById("empty-history-template");

const historyList = document.getElementById("history-list");
const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const submitButton = document.getElementById("submit-button");
const sentimentsList = document.getElementById("sentiments-list");
const responseElement = document.getElementById("response");
const generateSeedButton = document.getElementById("generate-seed-button");
const toastsContainer = document.getElementById("toasts");
const analysisContainer = document.getElementById("analysis-container");
let seedElement = document.getElementById("seed");

const fetchAsync = async (pathname, options) => {
  const response = await fetch(`/api/${pathname}`, options);
  if (!response.ok) throw new Error(response.status);

  return response;
};

const api = {
  analyze: (topic, seed, message) =>
    fetchAsync("analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ topic, seed, message }),
    }).then((response) => response.json()),
  getSeed: () =>
    fetchAsync("seed", { method: "GET" }).then((response) => response.json()),
  getResults: () =>
    fetchAsync("results", { method: "GET" }).then((response) =>
      response.json()
    ),
  deleteResult: (id) => fetchAsync(`results/${id}`, { method: "DELETE" }),
};

const TOAST_TIMEOUT_MS = 5000;
const TOAST_EXIT_DURATION_MS = 300;

const SENTIMENT_RENDER_DATA = {
  emotion: {
    name: "Emotion",
    labels: {
      sadness: "Sad",
      joy: "Joy",
      love: "Love",
      anger: "Anger",
      fear: "Fear",
      surprise: "Surprise",
    },
  },
  offensive: {
    name: "Offensiveness",
    labels: {
      offensive: "Offensive",
      "non-offensive": "Not offensive",
    },
  },
  question: {
    name: "Intent",
    labels: {
      question: "Question",
      statement: "Statement",
    },
  },
  mental_health: {
    name: "Mental state",
    labels: {
      "bad mental state": "Bad",
      "good mental state": "Good",
      "neutral mental state": "Neutral",
    },
  },
};

const toPercent = (value) => `${(value * 100).toFixed(2)}%`;

const cloneTemplate = (template) => template.content.cloneNode(true);

/**
 *
 * @param {HTMLTemplateElement} template
 * @param {(clone: DocumentFragment, $: (selector: string) => HTMLElement) => void} mutator
 * @returns {HTMLElement}
 */
const withTemplate = (template, mutator) => {
  const clone = cloneTemplate(template);
  mutator((selector) => clone.querySelector(selector), clone);
  return clone;
};

const closeToast = (id) => {
  const toast = document.getElementById(id);
  if (!toast) return;

  toast.classList.add("toast-exit");
  setTimeout(() => toast.remove(), TOAST_EXIT_DURATION_MS);
};

const toastError = () => {
  const id = `toast-${Date.now()}`;

  const toast = withTemplate(errorDialogTemplate, ($) => {
    $("dialog").setAttribute("id", id);
    $("button").addEventListener("click", () => closeToast(id));
  });

  Array.from(toastsContainer.children).forEach((toast) =>
    closeToast(toast.getAttribute("id"))
  );

  toastsContainer.appendChild(toast);
  setTimeout(() => closeToast(id), TOAST_TIMEOUT_MS);
};

const renderSeedElement = () => {
  if (document.getElementById("seed")) return;

  const container = cloneTemplate(seedTemplate).firstElementChild;
  generateSeedButton.insertAdjacentElement("afterend", container);
  seedElement = document.getElementById("seed");
};

const renderSeed = (topic, text) => {
  if (!topic || !text) return seedElement?.parentElement.remove();

  renderSeedElement();
  seedElement.setAttribute("data-topic", topic);
  seedElement.innerText = text;
};

const getHistoryItemElement = (item) =>
  withTemplate(historyItemTemplate, ($) => {
    $(".history-item-timestamp").innerText = new Date(
      item.created_at
    ).toLocaleString();

    const seedElement = $(".history-item-seed");
    seedElement.setAttribute("data-topic", item.topic);
    seedElement.innerText = item.seed;

    $(".history-item-message").innerText = item.message;

    const replyElement = $(".history-item-reply");

    if (item.results.should_reply) {
      replyElement.innerText = item.reply || "No reply";
    } else {
      const botOffIcon = withTemplate(botOffIconTemplate, ($) => {
        $("svg").classList.add("mt-0.5", "size-4", "shrink-0");
      });

      $(".bot-icon").replaceWith(botOffIcon);

      replyElement.parentNode.classList.add("text-zinc-400");
      replyElement.innerText = "Needs human intervention";
    }

    if (!item.reply) replyElement.classList.add("italic");

    $(".history-item-delete").addEventListener("click", async (e) => {
      try {
        await api.deleteResult(item.id);
        historyList.removeChild(e.target.closest(".history-item"));
        renderEmptyHistoryIndicator();
      } catch (error) {
        console.error(error);
        toastError();
      }
    });

    $(".history-item-restore").addEventListener("click", () => {
      renderSentiments(item.results.sentiments);
      renderReply(item.results.should_reply, item.reply);
      renderSeed(item.topic, item.seed);
      messageInput.value = item.message;
      messageInput.dispatchEvent(new Event("input"));
      messageInput.focus();
    });
  });

const renderHistoryItem = (item) => {
  document.getElementById("empty-history")?.remove();
  const element = getHistoryItemElement(item);
  historyList.appendChild(element);
};

const renderEmptyHistoryIndicator = () => {
  if (historyList.children.length === 0)
    historyList.appendChild(cloneTemplate(emptyHistoryTemplate));
};

const fetchAndRenderHistory = async () => {
  historyList.replaceChildren(
    withTemplate(loaderTemplate, ($) => {
      $("p").innerText = "Loading history...";
      $("div").classList.add("mt-2");
    })
  );

  try {
    const history = await api.getResults();
    historyList.replaceChildren(...history.map(getHistoryItemElement));
    renderEmptyHistoryIndicator();
  } catch (error) {
    console.error(error);
    toastError();
    historyList.replaceChildren();
  }
};

const renderSentiments = (sentiments) => {
  const elements = sentiments.map((sentiment) => {
    const { name, labels } = SENTIMENT_RENDER_DATA[sentiment.sentiment];

    return withTemplate(sentimentTemplate, ($) => {
      $(".sentiment-name").innerText = name;
      $(".sentiment-label").innerText = labels[sentiment.major];
      $(".sentiment-score").innerText = toPercent(sentiment.score);
    });
  });

  sentimentsList.replaceChildren(...elements);
};

const renderReply = (shouldReply, reply) => {
  if (!shouldReply) {
    responseElement.replaceChildren(cloneTemplate(fallbackTemplate));
  } else {
    responseElement.replaceChildren(
      withTemplate(responseTemplate, ($) => {
        $("p").innerText = reply;
      })
    );
  }
};

const setSentimentsLoading = (loading) => {
  if (loading) {
    setElementEnabled(submitButton, false);
    setElementEnabled(messageInput, false);
    setElementEnabled(generateSeedButton, false);
    sentimentsList.classList.add("animate-pulse");
    analysisContainer.classList.add("opacity-50");
  } else {
    setElementEnabled(submitButton, true);
    setElementEnabled(messageInput, true);
    setElementEnabled(generateSeedButton, true);
    sentimentsList.classList.remove("animate-pulse");
    analysisContainer.classList.remove("opacity-50");
  }
};

const setElementEnabled = (element, enabled) => {
  if (enabled) {
    element.removeAttribute("disabled");
    element.ariaDisabled = null;
  } else {
    element.setAttribute("disabled", "");
    element.ariaDisabled = "true";
  }
};

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event("submit"));
  }
});

messageInput.addEventListener("input", (e) => {
  setElementEnabled(submitButton, Boolean(e.target.value.trim()));
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const message = new FormData(e.target).get("message")?.toString().trim();
  if (!message) return;

  const seed = seedElement?.innerText;
  const topic = seedElement?.getAttribute("data-topic");

  setSentimentsLoading(true);

  try {
    const analysis = await api.analyze(topic, seed, message);

    renderReply(analysis.results.should_reply, analysis.reply);
    renderSentiments(analysis.results.sentiments);
    renderHistoryItem(analysis);
  } catch (error) {
    console.error(error);
    toastError();
  } finally {
    setSentimentsLoading(false);
    messageInput.focus();
  }
});

generateSeedButton.addEventListener("click", async () => {
  setElementEnabled(generateSeedButton, false);
  renderSeedElement();
  seedElement.replaceChildren(cloneTemplate(loaderTemplate));

  try {
    const { topic, text } = await api.getSeed();
    renderSeed(topic, text);
    messageInput.focus();
  } catch (error) {
    console.error(error);
    toastError();
    seedElement?.parentElement.remove();
  } finally {
    setElementEnabled(generateSeedButton, true);
  }
});

fetchAndRenderHistory();
