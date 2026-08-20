/* Injects shared navbar and footer into every page */
(function () {
  const NAV = `
<nav id="navbar">
  <div class="container nav-inner">
    <a class="nav-logo" href="index.html">
      <span class="logo-emoji">🐧</span>
      <span><b>Snow Place</b> Like Home</span>
    </a>
    <div class="nav-links">
      <a href="index.html">Home</a>
      <a href="game.html">Our Game</a>
      <a href="levels.html">Levels</a>
      <a href="how-to-play.html">How to Play</a>
      <a href="endless.html">Endless Mode</a>
      <a href="about.html">About Us</a>
      <a href="contact.html">Contact</a>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Menu">☰</button>
  </div>
  <div class="nav-mobile" id="navMobile">
    <a href="index.html">Home</a>
    <a href="game.html">Our Game</a>
    <a href="levels.html">Levels</a>
    <a href="how-to-play.html">How to Play</a>
    <a href="endless.html">Endless Mode</a>
    <a href="about.html">About Us</a>
    <a href="contact.html">Contact</a>
    <a href="faq.html">FAQ</a>
    <a href="gallery.html">Gallery</a>
  </div>
</nav>`;

  const FOOTER = `
<footer>
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>🐧 <span>Snow Place</span> Like Home</h3>
        <p>One penguin. Three worlds. One journey home. Can you make it back to the Arctic?</p>
      </div>
      <div class="footer-col">
        <h4>Game</h4>
        <a href="game.html">Our Game</a>
        <a href="levels.html">Levels</a>
        <a href="how-to-play.html">How to Play</a>
        <a href="endless.html">Endless Mode</a>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <a href="about.html">About Us</a>
        <a href="reviews.html">Reviews</a>
        <a href="gallery.html">Gallery</a>
      </div>
      <div class="footer-col">
        <h4>Info</h4>
        <a href="contact.html">Contact</a>
        <a href="faq.html">FAQ</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 Snow Place Like Home · Student Game Development Project</p>
      <p>🐧 One penguin. Three worlds. One journey home.</p>
    </div>
  </div>
</footer>
<button id="btt" title="Back to top">↑</button>`;

  // Insert nav before body content
  const navHolder = document.getElementById('nav-placeholder');
  if (navHolder) navHolder.outerHTML = NAV;

  const footerHolder = document.getElementById('footer-placeholder');
  if (footerHolder) footerHolder.outerHTML = FOOTER;
})();
