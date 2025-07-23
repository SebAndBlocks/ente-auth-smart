let hasTriggeredOTP = false;

function isLikelyOTPField(input) {
  const name = input.name?.toLowerCase() || "";
  const id = input.id?.toLowerCase() || "";
  const autocomplete = input.autocomplete?.toLowerCase() || "";

  return (
    name.includes("otp") ||
    name.includes("2fa") ||
    id.includes("otp") ||
    id.includes("2fa") ||
    autocomplete === "one-time-code"
  );
}

document.addEventListener("focusin", (e) => {
  const target = e.target;
  if (
    !hasTriggeredOTP &&
    target.tagName === "INPUT" &&
    isLikelyOTPField(target)
  ) {
    hasTriggeredOTP = true;

    chrome.runtime.sendMessage({ type: "open_ente_auth" });
  }
});
