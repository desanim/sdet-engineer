/**
 * VibeResume AI Client Bundle
 * WARNING: Realistic sample of a common Vibe-Coding mistake where backend secrets are bundled into client code.
 */
console.log("VibeResume AI Client Initialized");

// --- CRITICAL VIBE-CODING VULNERABILITY: LEAKED CREDENTIALS IN FRONTEND CODE ---
const STRIPE_SECRET_KEY = "sk_test_51MzSAMPLESTRIPESECRETKEYabcdefghijklmnop";
const OPENAI_API_KEY = "sk-proj-9999888877776666555544443333222211110000aaaaabbbbbcccccdddddeeeeefffffggggghhhhh";

document.addEventListener("DOMContentLoaded", () => {
  const ctaBtn = document.getElementById("cta-generate-btn");
  if (ctaBtn) {
    ctaBtn.addEventListener("click", async () => {
      ctaBtn.textContent = "Generating...";
      try {
        const res = await fetch("/api/generate");
        const data = await res.json();
        alert("Resume Generated Successfully! ID: " + data.id);
      } catch (e) {
        alert("Generation failed: " + e.message);
      } finally {
        ctaBtn.textContent = "Generate Resume Now";
      }
    });
  }
});
