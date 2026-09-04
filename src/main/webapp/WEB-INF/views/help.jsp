<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<% request.setAttribute("pageTitle", "Staff Help Guide"); %>
<%@ include file="../jspf/app-start.jspf" %>
<section class="help-hero">
    <div><p class="eyebrow eyebrow--light">NEW STAFF QUICK START</p><h2>Welcome to Sunrise Dental.</h2><p>Follow these simple steps to register patients, find records and print accurate bills.</p></div>
    <span class="help-hero__mark">?</span>
</section>

<section class="help-grid">
    <article class="help-step"><span class="help-step__number">1</span><div><h3>Sign in securely</h3><p>Open the system login page and enter the authorized staff username and password. Never share the password with patients or unauthorized people.</p><div class="help-tip"><b>Tip</b> Always use “Exit system safely” when leaving the desk.</div></div></article>
    <article class="help-step"><span class="help-step__number">2</span><div><h3>Register an appointment</h3><p>Select <strong>New appointment</strong>. Confirm the suggested appointment number, enter all patient details, then choose the dentist, treatment, date and time.</p><div class="help-tip"><b>Check</b> Required fields are marked with an orange asterisk.</div></div></article>
    <article class="help-step"><span class="help-step__number">3</span><div><h3>Find patient details</h3><p>Select <strong>Find appointment</strong>, enter a number such as APT-1001, and choose <strong>Search record</strong>. The complete appointment will appear.</p><div class="help-tip"><b>Note</b> Search is not case-sensitive.</div></div></article>
    <article class="help-step"><span class="help-step__number">4</span><div><h3>Calculate and print a bill</h3><p>Open <strong>Billing</strong> or continue from a patient record. The system adds the treatment charge and LKR 1,500 consultation fee automatically. Review, then select <strong>Print receipt</strong>.</p><div class="help-tip"><b>Check</b> Confirm the patient and treatment before printing.</div></div></article>
    <article class="help-step"><span class="help-step__number">5</span><div><h3>Handle an error message</h3><p>Read the highlighted message and correct the related field. A dentist cannot have two appointments at the same date and time, and appointment numbers must be unique.</p><div class="help-tip"><b>Help</b> Ask the clinic manager if a record cannot be found.</div></div></article>
    <article class="help-step"><span class="help-step__number">6</span><div><h3>Exit the system</h3><p>Select <strong>Exit system safely</strong> at the bottom of the menu. This closes the staff session and returns to the login screen.</p><div class="help-tip"><b>Security</b> Do this before closing the browser.</div></div></article>
</section>

<section class="card assumptions-card">
    <div><p class="eyebrow">SYSTEM RULES</p><h2>Important clinic assumptions</h2></div>
    <ul><li>Clinic hours are 08:00 to 18:00.</li><li>The standard consultation fee is LKR 1,500.</li><li>Only the listed dentists and treatment types may be selected.</li><li>Patient data is stored securely in the clinic's MySQL database.</li></ul>
</section>
<%@ include file="../jspf/app-end.jspf" %>
