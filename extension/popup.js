document.getElementById("generate").onclick = () => {
  const company = document.getElementById("company").value.trim();
  const weeks = parseInt(document.getElementById("weeks").value, 10) || 8;

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(tabs[0].id, {
      type: "SHOW_ROADMAP",
      body: {
        company,
        weeks,
        user_level: "intermediate",
      },
    });
  });
};
