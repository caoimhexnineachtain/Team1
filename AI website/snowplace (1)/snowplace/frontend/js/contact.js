/* contact.js */
async function submitContact(e) {
  e.preventDefault();

  const form = document.getElementById("contactForm");
  const msg = document.getElementById("contactMsg");
  const btn = document.getElementById("cSubmitBtn");

  msg.textContent = "";
  msg.className = "form-msg";

  const name = document.getElementById("cName").value.trim();
  const email = document.getElementById("cEmail").value.trim();
  const subject = document.getElementById("cSubject").value.trim();
  const message = document.getElementById("cMessage").value.trim();

  // Validate required fields
  if (!name || !email || !subject || !message) {
    msg.textContent = "Please fill in all required fields.";
    msg.className = "form-msg error";
    return;
  }

  // Validate email
  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  if (!emailRe.test(email)) {
    msg.textContent = "Please enter a valid email address.";
    msg.className = "form-msg error";
    return;
  }

  // Disable button while sending
  btn.disabled = true;
  btn.textContent = "Sending...";

  try {
    // Collect all form data including the Web3Forms access key
    const formData = new FormData(form);

    // Send directly to Web3Forms
    const res = await fetch("https://api.web3forms.com/submit", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.success) {
      msg.textContent =
        "✅ Thanks! Your message has been sent. We'll be in touch soon.";

      msg.className = "form-msg success";

      // Reset form after successful submission
      form.reset();
    } else {
      msg.textContent =
        data.message || "Something went wrong. Please try again.";

      msg.className = "form-msg error";
    }

  } catch (err) {
    console.error("Contact form error:", err);

    msg.textContent =
      "Unable to send your message. Please check your internet connection and try again.";

    msg.className = "form-msg error";

  } finally {
    // Re-enable button
    btn.disabled = false;
    btn.textContent = "📬 Send Message";
  }
}