<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<%@ page import="java.util.Map,java.util.Set,lk.sunrise.dental.model.AppointmentMode,lk.sunrise.dental.web.WebUtil" %>
<% request.setAttribute("pageTitle", "Register New Appointment"); %>
<%@ include file="../jspf/app-start.jspf" %>
<%
    Map<String, String> errors = (Map<String, String>) request.getAttribute("errors");
    String[] dentists = (String[]) request.getAttribute("dentists");
    Set<String> treatments = (Set<String>) request.getAttribute("treatments");
    AppointmentMode[] appointmentModes = (AppointmentMode[]) request.getAttribute("appointmentModes");
    String selectedDentist = (String) request.getAttribute("dentistName");
    String selectedTreatment = (String) request.getAttribute("treatmentType");
    String selectedMode = (String) request.getAttribute("appointmentMode");
    if (selectedMode == null || selectedMode.isBlank()) { selectedMode = "PHYSICAL"; }
%>
<div class="section-intro">
    <div><p class="eyebrow">PATIENT VISIT</p><h2>Appointment information</h2><p>Complete all required fields. The system prevents duplicate numbers and dentist double-bookings.</p></div>
    <span class="required-note"><b>*</b> Required fields</span>
</div>

<% if (request.getAttribute("formError") != null) { %>
    <div class="alert alert--error wide" role="alert"><strong>Appointment not saved</strong><span><%= WebUtil.escapeHtml((String) request.getAttribute("formError")) %></span></div>
<% } %>

<form class="card appointment-form" action="<%= contextPath %>/appointments/new" method="post">
    <section class="form-section">
        <div class="form-section__title"><span>1</span><div><h3>Visit reference</h3><p>A unique number identifies this appointment.</p></div></div>
        <div class="form-grid form-grid--two">
            <label class="form-field">
                <span>Appointment number <b>*</b></span>
                <input class="input-highlight" type="text" name="appointmentNumber" required pattern="APT-[0-9]{4,6}"
                       value="<%= WebUtil.escapeHtml((String) request.getAttribute("appointmentNumber")) %>" placeholder="APT-1001">
                <% if (errors != null && errors.containsKey("appointmentNumber")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("appointmentNumber")) %></small><% } else { %><small>Format: APT- followed by 4 to 6 digits</small><% } %>
            </label>
            <div class="info-panel"><span>✓</span><p><strong>Duplicate protection is active.</strong><br>The number and dentist time slot are checked before saving.</p></div>
        </div>
    </section>

    <section class="form-section">
        <div class="form-section__title"><span>2</span><div><h3>Patient details</h3><p>Contact information used by reception staff.</p></div></div>
        <div class="form-grid form-grid--two">
            <label class="form-field">
                <span>Patient name <b>*</b></span>
                <input type="text" name="patientName" required maxlength="80" placeholder="Full name"
                       value="<%= WebUtil.escapeHtml((String) request.getAttribute("patientName")) %>">
                <% if (errors != null && errors.containsKey("patientName")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("patientName")) %></small><% } %>
            </label>
            <label class="form-field">
                <span>Contact number <b>*</b></span>
                <input type="tel" name="contactNumber" required placeholder="0771234567"
                       value="<%= WebUtil.escapeHtml((String) request.getAttribute("contactNumber")) %>">
                <% if (errors != null && errors.containsKey("contactNumber")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("contactNumber")) %></small><% } %>
            </label>
            <label class="form-field form-field--full">
                <span>Address <b>*</b></span>
                <textarea name="address" required maxlength="160" rows="3" placeholder="Patient residential address"><%= WebUtil.escapeHtml((String) request.getAttribute("address")) %></textarea>
                <% if (errors != null && errors.containsKey("address")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("address")) %></small><% } %>
            </label>
        </div>
    </section>

    <section class="form-section">
        <div class="form-section__title"><span>3</span><div><h3>Treatment & schedule</h3><p>Choose the dentist, treatment, visit method, date and time.</p></div></div>
        <div class="form-grid form-grid--two">
            <label class="form-field">
                <span>Dentist <b>*</b></span>
                <select name="dentistName" required>
                    <option value="">Select a dentist</option>
                    <% for (String dentist : dentists) { %><option value="<%= WebUtil.escapeHtml(dentist) %>" <%= dentist.equals(selectedDentist) ? "selected" : "" %>><%= WebUtil.escapeHtml(dentist) %></option><% } %>
                </select>
            </label>
            <label class="form-field">
                <span>Treatment type <b>*</b></span>
                <select name="treatmentType" required>
                    <option value="">Select a treatment</option>
                    <% for (String treatment : treatments) { %><option value="<%= WebUtil.escapeHtml(treatment) %>" <%= treatment.equals(selectedTreatment) ? "selected" : "" %>><%= WebUtil.escapeHtml(treatment) %></option><% } %>
                </select>
                <% if (errors != null && errors.containsKey("treatmentType")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("treatmentType")) %></small><% } %>
            </label>
            <fieldset class="form-field appointment-mode-field">
                <legend>Appointment method <b>*</b></legend>
                <div class="appointment-mode-options">
                    <% for (AppointmentMode mode : appointmentModes) { %>
                        <label class="appointment-mode-option <%= mode.name().equals(selectedMode) ? "appointment-mode-option--selected" : "" %>">
                            <input type="radio" name="appointmentMode" value="<%= mode.name() %>" required <%= mode.name().equals(selectedMode) ? "checked" : "" %>>
                            <span><strong><%= WebUtil.escapeHtml(mode.getDisplayName()) %></strong><small><%= mode == AppointmentMode.ONLINE ? "Remote consultation arranged by clinic staff" : "Attend the clinic in person" %></small></span>
                        </label>
                    <% } %>
                </div>
                <% if (errors != null && errors.containsKey("appointmentMode")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("appointmentMode")) %></small><% } %>
            </fieldset>
            <label class="form-field">
                <span>Appointment date <b>*</b></span>
                <input type="date" name="appointmentDate" required min="<%= request.getAttribute("today") %>"
                       value="<%= WebUtil.escapeHtml((String) request.getAttribute("appointmentDate")) %>">
                <% if (errors != null && errors.containsKey("appointmentDate")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("appointmentDate")) %></small><% } %>
            </label>
            <label class="form-field">
                <span>Appointment time <b>*</b></span>
                <input type="time" name="appointmentTime" required min="08:00" max="18:00" step="900"
                       value="<%= WebUtil.escapeHtml((String) request.getAttribute("appointmentTime")) %>">
                <% if (errors != null && errors.containsKey("appointmentTime")) { %><small class="field-error"><%= WebUtil.escapeHtml(errors.get("appointmentTime")) %></small><% } else { %><small>Clinic hours: 08:00–18:00</small><% } %>
            </label>
        </div>
    </section>

    <div class="form-actions">
        <a class="button button--secondary" href="<%= contextPath %>/dashboard">Cancel</a>
        <button class="button button--primary" type="submit">Save appointment <span>→</span></button>
    </div>
</form>
<%@ include file="../jspf/app-end.jspf" %>
