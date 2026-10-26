/**
 * Interactive DApp UI script with Keyboard, Focus & ARIA State Management
 */
document.addEventListener("DOMContentLoaded", () => {
  const payInput = document.getElementById("pay-amount-input");
  const receiveInput = document.getElementById("receive-amount-input");
  const executeBtn = document.getElementById("execute-swap-btn");
  const themeToggle = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");
  const connectWalletBtn = document.getElementById("connect-wallet-btn");
  
  // Modal elements
  const modal = document.getElementById("swap-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalCancelBtn = document.getElementById("modal-cancel-btn");
  const modalConfirmBtn = document.getElementById("modal-confirm-btn");
  
  const EXCHANGE_RATE = 3124.50;
  let previousActiveElement = null;

  // 1. Amount Calculation & Accessible Button State
  payInput.addEventListener("input", (e) => {
    const val = parseFloat(e.target.value);
    if (!isNaN(val) && val > 0) {
      receiveInput.value = (val * EXCHANGE_RATE).toFixed(2);
      executeBtn.disabled = false;
      executeBtn.setAttribute("aria-disabled", "false");
      executeBtn.textContent = "Swap";
    } else {
      receiveInput.value = "";
      executeBtn.disabled = true;
      executeBtn.setAttribute("aria-disabled", "true");
      executeBtn.textContent = "Enter an amount";
    }
  });

  // 2. Modal Open / Close with Focus Trap & Escape Key
  function openModal() {
    previousActiveElement = document.activeElement;
    modal.removeAttribute("hidden");
    // Move focus inside dialog (WCAG 2.4.3 Focus Order)
    modalConfirmBtn.focus();
    document.addEventListener("keydown", trapFocus);
  }

  function closeModal() {
    modal.setAttribute("hidden", "");
    document.removeEventListener("keydown", trapFocus);
    // Return focus to triggering button
    if (previousActiveElement) {
      previousActiveElement.focus();
    }
  }

  function trapFocus(e) {
    if (e.key === "Escape") {
      closeModal();
      return;
    }

    if (e.key === "Tab") {
      const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );
      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    }
  }

  executeBtn.addEventListener("click", openModal);
  modalCloseBtn.addEventListener("click", closeModal);
  modalCancelBtn.addEventListener("click", closeModal);
  modalConfirmBtn.addEventListener("click", () => {
    alert("Transaction submitted to Ethereum Mempool!");
    closeModal();
  });

  // 3. Accessible Theme Toggle (Light/Dark mode)
  themeToggle.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-theme");
    document.body.classList.toggle("light-theme", !isDark);
    themeToggle.setAttribute("aria-pressed", String(isDark));
    themeIcon.textContent = isDark ? "🌙" : "☀️";
  });

  // 4. Connect Wallet Mock
  connectWalletBtn.addEventListener("click", () => {
    connectWalletBtn.textContent = "0x742d...f44e";
    connectWalletBtn.classList.remove("btn-primary");
    connectWalletBtn.classList.add("btn-secondary");
    connectWalletBtn.setAttribute("aria-label", "Connected as Ethereum Address 0x742d...f44e");
  });
});
