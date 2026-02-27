
const sidebarCSS = `
  #ai-mentor-sidebar {
    position: fixed !important;
    top: 80px !important;
    right: 0 !important;
    width: 350px !important;
    height: 70vh !important;
    background: #ffffff !important;
    color: #000 !important;
    border-left: 2px solid #ccc !important;
    z-index: 99999999 !important;
    padding: 12px !important;
    overflow-y: auto !important;
    font-family: sans-serif !important;
  }
`;

function injectStyle() {
  if (!document.getElementById("ai-mentor-style")) {
    const style = document.createElement("style");
    style.id = "ai-mentor-style";
    style.innerText = sidebarCSS;
    document.head.appendChild(style);
  }
}

function injectSidebar() {
  injectStyle();

  if (!document.getElementById("ai-mentor-sidebar")) {
    const box = document.createElement("div");
    box.id = "ai-mentor-sidebar";

    box.innerHTML = `
      <h2 style="font-size:20px; font-weight:bold;">AI Mentor</h2>
      <div id="ai-content" style="margin-top:10px; font-size:14px;">
        Detecting problem...
      </div>
    `;

    document.body.appendChild(box);
  }
}


setInterval(() => {
  injectSidebar();
  autoDetectProblem();
}, 800);




let lastDetectedProblem = "";

function getProblemTitle() {
  // 1. Extract directly from <title> tag
  const pageTitle = document.querySelector("title")?.innerText;
  if (pageTitle && pageTitle.includes(" - LeetCode")) {
    return pageTitle.replace(" - LeetCode", "").trim();
  }

  // 2. URL fallback
  const slug = window.location.pathname.split("/problem/")[1];
  if (slug) {
    return slug.split("/")[0].replace(/-/g, " ");
  }

  // 3. Your URL structure is different → /problems/<slug>/description/
  const slug2 = window.location.pathname.split("/problems/")[1];
  if (slug2) {
    return slug2.split("/")[0].replace(/-/g, " ");
  }

  return null;
}



function autoDetectProblem() {
  const title = getProblemTitle();

  if (!title || title.length < 2) return;

  if (title === lastDetectedProblem) return; // avoid duplicate calls
  lastDetectedProblem = title;

  const sidebar = document.getElementById("ai-content");
  if (sidebar) {
    sidebar.innerText = `Detected: ${title}\nFetching hints...`;
  }

  // Send to popup/backend via background script
  chrome.runtime.sendMessage(
    {
      type: "AUTO_HINT",
      problem_title: title,
    },
    (resp) => {
      if (!resp) return;

      if (resp.ok) {
        document.getElementById("ai-content").innerText =
          resp.data.hint_text;
      } else {
        document.getElementById("ai-content").innerText =
          "Error fetching hints: " + resp.err;
      }
    }
  );
}


// ==========================
// Handle manual roadmap from popup
// ==========================
chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === "SHOW_ROADMAP") {
    document.getElementById("ai-content").innerText = "Loading roadmap...";

    chrome.runtime.sendMessage(
      {
        type: "GET_ROADMAP",
        body: msg.body,
      },
      (resp) => {
        if (resp.ok) {
          document.getElementById("ai-content").innerText =
            resp.data.roadmap_text;
        } else {
          document.getElementById("ai-content").innerText =
            "Error: " + resp.err;
        }
      }
    );
  }
});
