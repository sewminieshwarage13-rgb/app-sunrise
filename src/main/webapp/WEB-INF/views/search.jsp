<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<%@ page import="java.time.format.DateTimeFormatter,lk.sunrise.dental.model.Appointment,lk.sunrise.dental.web.WebUtil" %>
<% request.setAttribute("pageTitle", "Find Appointment"); %>
<%@ include file="../jspf/app-start.jspf" %>
<%
    Appointment appointment = (Appointment) request.getAttribute("appointment");
    DateTimeFormatter dateFormat = DateTimeFormatter.ofPattern("EEEE, dd MMMM yyyy");
    DateTimeFormatter timeFormat = DateTimeFormatter.ofPattern("hh:mm a");
%>
<section class="search-hero card">
    <div><p class="eyebrow">QUICK RECORD LOOKUP</p><h2>Search by appointment number</h2><p>Enter the unique reference printed on the patient’s appointment.</p></div>
    <form class="search-box" action="<%= contextPath %>/appointments/search" method="get">
        <label class="sr-only" for="appointment-search">Appointment number</label>
        <span>⌕</span><input id="appointment-search" type="text" name="number" required placeholder="e.g. APT-1001" value="<%= WebUtil.escapeHtml((String) request.getAttribute("number")) %>">
        <button class="button button--primary" type="submit">Search record</button>
    </form>
</section>

<% if (request.getParameter("created") != null && appointment != null) { %>
    <div class="alert alert--success wide" role="status"><strong>Appointment registered successfully</strong><span>The patient record is now safely stored.</span></div>
<% } %>

<% if (request.getAttribute("notFound") != null) { %>
    <section class="card empty-state"><span>⌕</span><h2>No appointment found</h2><p>Check the number “<strong><%= WebUtil.escapeHtml((String) request.getAttribute("number")) %></strong>” and try again.</p></section>
<% } else if (appointment != null) { %>
    <section class="record-card card">
        <div class="record-card__top">
            <div><p class="eyebrow">APPOINTMENT RECORD</p><h2><%= WebUtil.escapeHtml(appointment.getPatientName()) %></h2><span class="record-number"><%= WebUtil.escapeHtml(appointment.getAppointmentNumber()) %></span></div>
            <span class="status-pill"><i></i> Confirmed</span>
        </div>
        <div class="schedule-highlight">
            <div><span class="detail-icon">▣</span><span><small>Appointment date</small><strong><%= appointment.getAppointmentDate().format(dateFormat) %></strong></span></div>
            <div><span class="detail-icon">◷</span><span><small>Appointment time</small><strong><%= appointment.getAppointmentTime().format(timeFormat) %></strong></span></div>
        </div>
        <div class="details-grid">
            <div class="detail-item"><small>Patient name</small><strong><%= WebUtil.escapeHtml(appointment.getPatientName()) %></strong></div>
            <div class="detail-item"><small>Contact number</small><strong><%= WebUtil.escapeHtml(appointment.getContactNumber()) %></strong></div>
            <div class="detail-item detail-item--full"><small>Address</small><strong><%= WebUtil.escapeHtml(appointment.getAddress()) %></strong></div>
            <div class="detail-item"><small>Dentist</small><strong><%= WebUtil.escapeHtml(appointment.getDentistName()) %></strong></div>
            <div class="detail-item"><small>Treatment type</small><strong><%= WebUtil.escapeHtml(appointment.getTreatmentType()) %></strong></div>
            <div class="detail-item detail-item--full"><small>Appointment method</small><strong><%= WebUtil.escapeHtml(appointment.getAppointmentMode().getDisplayName()) %></strong></div>
        </div>
        <div class="record-actions">
            <a class="button button--secondary" href="<%= contextPath %>/appointments/search">Search another</a>
            <a class="button button--primary" href="<%= contextPath %>/bill?number=<%= WebUtil.escapeHtml(appointment.getAppointmentNumber()) %>">Calculate patient bill <span>→</span></a>
        </div>
    </section>
<% } else { %>
    <section class="search-tips">
        <article><span>1</span><div><strong>Enter the reference</strong><p>Use the full number, including APT-.</p></div></article>
        <article><span>2</span><div><strong>Review the record</strong><p>Confirm patient, treatment and time.</p></div></article>
        <article><span>3</span><div><strong>Create the bill</strong><p>Continue directly to the receipt.</p></div></article>
    </section>
<% } %>
<%@ include file="../jspf/app-end.jspf" %>
