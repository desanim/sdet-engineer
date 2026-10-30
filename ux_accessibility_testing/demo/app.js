const form = document.querySelector('#swap-form');
const amount = document.querySelector('#amount');
const error = document.querySelector('#amount-error');
const estimate = document.querySelector('#estimate');
const dialog = document.querySelector('#review-dialog');
const review = document.querySelector('#review');
const status = document.querySelector('#status');
const valid = () => amount.validity.valid && Number(amount.value) > 0 && Number.isFinite(Number(amount.value));
function clearError() { error.hidden = true; error.textContent = ''; amount.removeAttribute('aria-invalid'); }
amount.addEventListener('input', () => {
  clearError();
  estimate.value = valid() ? (Number(amount.value) * 3124.5).toFixed(2) : '0.00';
  status.textContent = '';
});
form.addEventListener('submit', event => {
  event.preventDefault();
  if (!valid()) {
    error.textContent = 'Enter an amount greater than 0 and no more than 5 ETH.';
    error.hidden = false; amount.setAttribute('aria-invalid', 'true'); amount.focus(); return;
  }
  clearError();
  document.querySelector('#dialog-description').textContent = `Simulate swapping ${amount.value} ETH for ${estimate.value} USDC. No funds will move.`;
  dialog.showModal();
});
document.querySelector('#cancel').addEventListener('click', () => dialog.close('cancel'));
document.querySelector('#confirm').addEventListener('click', () => {
  status.textContent = 'Simulation complete. No transaction was broadcast.'; dialog.close('confirm');
});
dialog.addEventListener('close', () => review.focus());
// Explicit focus destination for skip link; negative tabindex keeps main out of Tab order.
document.querySelector('#skip').addEventListener('click', () => document.querySelector('#main').focus());

// Keep Tab cycling within the two enabled actions without a stop in browser chrome.
dialog.addEventListener('keydown', event => {
  if (event.key !== 'Tab') return;
  const first = document.querySelector('#cancel');
  const last = document.querySelector('#confirm');
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
  else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
});
