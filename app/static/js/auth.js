async function signup() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const res = await fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok) {
      alert(data.message || "Signup successful");
      window.location.href = "/login.html";
    } else {
      alert(data.detail || data.message || "Signup failed");
    }

  } catch (error) {
    console.warn("Backend unavailable, using offline signup:", error);

    // FALLBACK SIGNUP
    let users = JSON.parse(localStorage.getItem("users")) || {};

    if (users[email]) {
      alert("User already exists (Offline Mode)");
      return;
    }

    users[email] = password;
    localStorage.setItem("users", JSON.stringify(users));

    alert("Signup successful (Offline Mode)");
    window.location.href = "/login.html";
  }
}

async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    alert("Please enter email and password");
    return;
  }

  try {
    const res = await fetch("/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();

    if (res.ok && (data.message === "Login successful" || data.success)) {
      localStorage.setItem("user_id", email);
      window.location.href = "/dashboard.html";
    } else {
      alert(data.detail || data.message || "Invalid credentials");
    }

  } catch (error) {
    console.warn("Backend unavailable, using offline login:", error);

    // FALLBACK LOGIN
    let users = JSON.parse(localStorage.getItem("users")) || {};

    if (users[email] === password) {
      localStorage.setItem("user_id", email);
      window.location.href = "/dashboard.html";
    } else {
      alert("Invalid credentials");
    }
  }
}