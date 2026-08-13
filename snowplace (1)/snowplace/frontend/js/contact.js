/* contact.js */
async function submitContact(e) {
  e.preventDefault();
  const msg  = document.getElementById('contactMsg');
  const btn  = document.getElementById('cSubmitBtn');
  msg.className = 'form-msg';

  const name    = document.getElementById('cName').value.trim();
  const email   = document.getElementById('cEmail').value.trim();
  const subject = document.getElementById('cSubject').value.trim();
  const message = document.getElementById('cMessage').value.trim();

  if (!name || !email || !subject || !message) {
    msg.textContent = 'Please fill in all required fields.';
    msg.className = 'form-msg error'; return;
  }
  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRe.test(email)) {
    msg.textContent = 'Please enter a valid email address.';
    msg.className = 'form-msg error'; return;
  }

  btn.disabled = true; btn.textContent = 'Sending...';
  try {
    const res  = await fetch('/api/contact', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ name, email, subject, message })
    });
    const data = await res.json();
    if (data.success) {
      msg.textContent = '✅ Thanks! Your message has been sent. We\'ll be in touch soon.';
      msg.className = 'form-msg success';
      document.getElementById('contactForm').reset();
    } else {
      msg.textContent = data.error || 'Something went wrong.';
      msg.className = 'form-msg error';
    }
  } catch (err) {
    msg.textContent = 'Server not reachable. Please make sure the server is running.';
    msg.className = 'form-msg error';
  } finally {
    btn.disabled = false; btn.textContent = '📬 Send Message';
  }
}
