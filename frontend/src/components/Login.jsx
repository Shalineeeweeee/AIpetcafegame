import React from "react";
import "./Login.css";

function Login() {
  return (
    <div className="login-page">
      <div className="login-container">
        <h1 className="game-title">
          <span className="golden">WELCOME TO</span> <span className="farm">CAFE</span>
        </h1>
        <div className="login-box">
          <h2>Sign In</h2>
          <div className="input-group">
            <input type="text" placeholder="Username" />
          </div>
          <div className="input-group">
            <input type="password" placeholder="Password" />
          </div>
          <button className="login-btn">Enter</button>
          <p className="social-signin">or Sign In with</p>
          <p className="register-link">Don't have an account? <a>Register</a></p>
        </div>
      </div>
    </div>
  );
}

export default Login;