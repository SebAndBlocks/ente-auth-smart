chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "open_ente_auth") {
    fetch("http://127.0.0.1:8765/popup").catch((err) =>
      console.error("Ente Auth Smart Extension: Failed to contact local server:", err)
    );
  }
});
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "open-ente-auth",
    title: "Open Ente Auth",
    contexts: ["all"]
  });
});