<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<%@ page import="lk.sunrise.dental.web.WebUtil" %>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Staff Login | Sunrise Dental Clinic</title>
    <link rel="stylesheet" href="<%= request.getContextPath() %>/assets/app.css">
</head>
<body class="login-page">
<div class="login-decoration login-decoration--one"></div>
<div class="login-decoration login-decoration--two"></div>
<main class="login-layout">
    <section class="login-intro">
        <a class="brand brand--light" href="#" aria-label="Sunrise Dental Clinic">
            <span class="brand__mark">S+</span>
            <span><strong>Sunrise</strong><small>Dental Clinic</small></span>
        </a>
        <div>
            <p class="eyebrow eyebrow--light">WELCOME TO A BRIGHTER WORKDAY</p>
            <h1>Simple care starts with an organised clinic.</h1>
            <p>Securely manage appointments, patient details and accurate treatment bills in one place.</p>
        </div>
        <div class="login-feature-row">
            <span>✓ Secure access</span><span>✓ Fewer booking errors</span><span>✓ Faster billing</span>
        </div>
    </section>

    <section class="login-panel">
        <div class="login-card">
            <div class="mobile-brand">
                <span class="brand__mark">S+</span><strong>Sunrise Dental</strong>
            </div>
            <p class="eyebrow">AUTHORIZED STAFF ONLY</p>
            <h2>Sign in to continue</h2>
            <p class="muted">Enter your staff account details to access the clinic system.</p>

            <% if (request.getAttribute("error") != null) { %>
                <div class="alert alert--error" role="alert">
                    <strong>Login unsuccessful</strong>
                    <span><%= WebUtil.escapeHtml((String) request.getAttribute("error")) %></span>
                </div>
            <% } else if (request.getParameter("logout") != null) { %>
                <div class="alert alert--success" role="status">
                    <strong>Signed out safely</strong><span>Your staff session has ended.</span>
                </div>
            <% } else if (request.getParameter("expired") != null) { %>
                <div class="alert alert--warning" role="alert">
                    <strong>Session ended</strong><span>Please sign in again to continue.</span>
                </div>
            <% } %>

            <form class="form-stack" action="<%= request.getContextPath() %>/login" method="post">
                <label class="form-field">
                    <span>Username</span>
                    <input type="text" name="username" autocomplete="username" required autofocus
                           placeholder="Enter username"
                           value="<%= WebUtil.escapeHtml((String) request.getAttribute("username")) %>">
                </label>
                <label class="form-field">
                    <span>Password</span>
                    <input type="password" name="password" autocomplete="current-password" required
                           placeholder="Enter password">
                </label>
                <button class="button button--primary button--large" type="submit">Sign in securely <span>→</span></button>
            </form>
            <div class="demo-hint">
                <span class="demo-hint__icon">i</span>
                <span><strong>Assessment demo:</strong> admin / Sunrise@123</span>
            </div>
        </div>
        <p class="login-footer">Sunrise Dental Clinic • Colombo, Sri Lanka</p>
    </section>
</main>
</body>
</html>
