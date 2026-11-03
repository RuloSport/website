// RuloSport site behaviour: product gallery, pack selector, and forms.

// Paste the Formspree form URL here once it's set up (e.g. "https://formspree.io/f/abcdwxyz").
// Until then, forms open a pre-filled email to sales@rulosport.com instead.
const FORM_ENDPOINT = "https://formspree.io/f/xbggqler";
const SALES_EMAIL = "sales@rulosport.com";

// Gallery thumbnails
document.querySelectorAll("[data-gallery]").forEach((gallery) => {
  const main = gallery.querySelector(".gallery-main img");
  gallery.querySelectorAll(".thumbs button").forEach((btn) => {
    btn.addEventListener("click", () => {
      main.src = btn.dataset.src;
      main.alt = btn.dataset.alt || main.alt;
      gallery.querySelectorAll(".thumbs button").forEach((b) => b.setAttribute("aria-pressed", "false"));
      btn.setAttribute("aria-pressed", "true");
    });
  });
});

// Pack size selector: updates price and the DemoPadel buy link
document.querySelectorAll("[data-variants]").forEach((set) => {
  const price = document.querySelector("[data-price]");
  const buy = document.querySelector("[data-buy]");
  set.addEventListener("change", (e) => {
    const opt = e.target;
    if (!opt.dataset) return;
    if (price && opt.dataset.price) price.firstChild.textContent = opt.dataset.price + " ";
    if (buy && opt.dataset.url) buy.href = opt.dataset.url;
  });
});

// Forms
function formToText(form) {
  const lines = [];
  new FormData(form).forEach((value, key) => {
    if (key.startsWith("_") || String(value).trim() === "") return;
    lines.push(`${key}: ${value}`);
  });
  return lines.join("\n");
}

document.querySelectorAll("form[data-rulo-form]").forEach((form) => {
  const status = form.querySelector(".form-status");
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (form.dataset.needsQty !== undefined) {
      const any = [...form.querySelectorAll('input[type="number"]')].some((i) => Number(i.value) > 0);
      if (!any) {
        status.className = "form-status err";
        status.textContent = "Add a quantity for at least one product.";
        return;
      }
    }
    if (form.dataset.moq) {
      const moq = Number(form.dataset.moq);
      const short = [...form.querySelectorAll('input[type="number"]')].filter((i) => Number(i.value) > 0 && Number(i.value) < moq);
      if (short.length) {
        const names = short.map((i) => i.closest("tr").cells[0].textContent).join(", ");
        status.className = "form-status err";
        status.textContent = `The minimum order is ${moq} units per product. Increase the quantity for: ${names}.`;
        short[0].focus();
        return;
      }
    }
    const subject = form.dataset.subject || "Website enquiry";
    if (!FORM_ENDPOINT) {
      const body = encodeURIComponent(formToText(form));
      window.location.href = `mailto:${SALES_EMAIL}?subject=${encodeURIComponent(subject)}&body=${body}`;
      status.className = "form-status";
      status.textContent = `Your email app should open with the details filled in. If it doesn't, email ${SALES_EMAIL}.`;
      return;
    }
    status.className = "form-status";
    status.textContent = "Sending…";
    try {
      const data = new FormData(form);
      data.append("_subject", subject);
      const res = await fetch(FORM_ENDPOINT, { method: "POST", body: data, headers: { Accept: "application/json" } });
      if (!res.ok) throw new Error(String(res.status));
      form.reset();
      status.className = "form-status ok";
      status.textContent = form.dataset.success || "Thanks, we've got it. We'll be in touch within one business day.";
    } catch (err) {
      status.className = "form-status err";
      status.textContent = `That didn't send. Please try again, or email ${SALES_EMAIL}.`;
    }
  });
});
