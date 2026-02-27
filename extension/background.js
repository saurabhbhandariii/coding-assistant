// background.js

chrome.runtime.onInstalled.addListener(() => {
  console.log("AI Coding Mentor installed.");
});

// Handle ROADMAP request (manual)
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "GET_ROADMAP") {
    fetch("http://localhost:8000/roadmap", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(msg.body),
    })
      .then((r) => r.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, err: err.message }));

    return true; // keep channel open
  }
});

// Handle AUTO HINT request
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === "AUTO_HINT") {
    fetch("http://localhost:8000/hint", {
      method: "POST",                      // IMPORTANT
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problem_title: msg.problem_title,
        description: "",
        user_code: ""
      }),
    })
      .then((r) => r.json())
      .then((data) => sendResponse({ ok: true, data }))
      .catch((err) => sendResponse({ ok: false, err: err.message }));

    return true;
  }
});
