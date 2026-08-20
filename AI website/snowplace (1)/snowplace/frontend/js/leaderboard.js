/* leaderboard.js — Endless Mode leaderboard */
// ============================================
// WEB3FORMS SCORE SUBMISSION
// ============================================

// PUT YOUR WEB3FORMS ACCESS KEY HERE
const WEB3FORMS_ACCESS_KEY = "95dba075-05f9-45f3-b4af-d1b725e92479";


async function submitScore() {

  // Get form values
  const name = document.getElementById("lbName").value.trim();
  const score = document.getElementById("lbScore").value;
  const cubes = document.getElementById("lbCubes").value || 0;
  const time = document.getElementById("lbTime").value || 0;

  const msg = document.getElementById("lbMsg");


  // Reset message
  msg.className = "form-msg";
  msg.textContent = "";


  // Validate
  if (!name) {

    msg.textContent = "Please enter your name.";
    msg.className = "form-msg error";

    return;
  }


  if (score === "" || Number(score) < 0) {

    msg.textContent = "Please enter a valid score.";
    msg.className = "form-msg error";

    return;
  }


  // Show submitting message
  msg.textContent = "Submitting your score...";
  msg.className = "form-msg";


  // Create Web3Forms data
  const formData = new FormData();


  // Web3Forms access key
  formData.append(
    "access_key",
    WEB3FORMS_ACCESS_KEY
  );


  // Email subject
  formData.append(
    "subject",
    `🏆 Endless Mode Score - ${name}`
  );


  // Sender name
  formData.append(
    "from_name",
    "Snow Place Like Home"
  );


  // Score information
  formData.append(
    "Player Name",
    name
  );

  formData.append(
    "Score",
    score
  );

  formData.append(
    "Ice Cubes Collected",
    cubes
  );

  formData.append(
    "Survival Time",
    `${time} seconds`
  );


  // Optional message
  formData.append(
    "message",
    `
Snow Place Like Home - Endless Mode

Player: ${name}
Score: ${score}
Ice Cubes: ${cubes}
Survival Time: ${time} seconds
    `
  );


  try {

    // Send to Web3Forms
    const response = await fetch(
      "https://api.web3forms.com/submit",
      {
        method: "POST",
        body: formData
      }
    );


    const data = await response.json();


    // Successful submission
    if (data.success) {

      msg.textContent =
        "🏆 Score submitted successfully!";

      msg.className =
        "form-msg success";


      // Clear form
      document.getElementById("lbName").value = "";
      document.getElementById("lbScore").value = "";
      document.getElementById("lbCubes").value = "";
      document.getElementById("lbTime").value = "";


    } else {

      msg.textContent =
        data.message || "Something went wrong.";

      msg.className =
        "form-msg error";

    }


  } catch (error) {

    console.error(
      "Web3Forms error:",
      error
    );


    msg.textContent =
      "Could not submit the score. Please try again.";

    msg.className =
      "form-msg error";

  }

}