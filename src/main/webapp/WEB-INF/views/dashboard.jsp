<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<%@ page import="java.util.List,java.time.format.DateTimeFormatter,lk.sunrise.dental.model.Appointment,lk.sunrise.dental.web.WebUtil" %>
<% request.setAttribute("pageTitle", "Dashboard"); %>
<%@ include file="../jspf/app-start.jspf" %>
<%
    long todayCount = (Long) request.getAttribute("todayCount");
    int totalCount = (Integer) request.getAttribute("totalCount");
    List<Appointment> upcoming = (List<Appointment>) request.getAttribute("upcoming");
    DateTimeFormatter displayDate = DateTimeFormatter.ofPattern("dd MMM yyyy");
    DateTimeFormatter displayTime = DateTimeFormatter.ofPattern("hh:mm a");
%>
<section class="welcome-banner">
    <div>
        <span class="welcome-banner__label">CLINIC OVERVIEW</span>
        <h2>Good day, <%= WebUtil.escapeHtml(currentUser) %>.</h2>
        <p>Everything you need to keep today’s patient visits running smoothly.</p>
    </div>
    <a class="button button--white" href="<%= contextPath %>/appointments/new">＋ Register appointment</a>
</section>

<section class="stats-grid" aria-label="Appointment statistics">
    <article class="stat-card stat-card--orange">
        <span class="stat-card__icon">◷</span>
        <div><strong><%= todayCount %></strong><span>Appointments today</span></div>
    </article>
    <article class="stat-card stat-card--teal">
        <span class="stat-card__icon">▤</span>
        <div><strong><%= totalCount %></strong><span>Total records</span></div>
    </article>
    <article class="stat-card stat-card--blue">
        <span class="stat-card__icon">#</span>
        <div><strong><%= WebUtil.escapeHtml((String) request.getAttribute("nextNumber")) %></strong><span>Next appointment no.</span></div>
    </article>
</section>

<section class="content-grid">
    <article class="card span-two">
        <div class="card__header">
            <div><p class="eyebrow">SCHEDULE</p><h2>Upcoming appointments</h2></div>
            <a class="text-link" href="<%= contextPath %>/appointments/search">Find a record →</a>
        </div>
        <% if (upcoming.isEmpty()) { %>
            <div class="empty-state compact">
                <span>☀</span><h3>No appointments yet</h3>
                <p>Register the first patient visit to begin today’s schedule.</p>
            </div>
        <% } else { %>
            <div class="appointment-list">
                <% for (Appointment item : upcoming) { %>
                    <a class="appointment-row" href="<%= contextPath %>/appointments/search?number=<%= WebUtil.escapeHtml(item.getAppointmentNumber()) %>">
                        <div class="date-tile"><strong><%= item.getAppointmentDate().getDayOfMonth() %></strong><span><%= item.getAppointmentDate().getMonth().toString().substring(0, 3) %></span></div>
                        <div class="appointment-row__main"><strong><%= WebUtil.escapeHtml(item.getPatientName()) %></strong><span><%= WebUtil.escapeHtml(item.getTreatmentType()) %> • <%= WebUtil.escapeHtml(item.getDentistName()) %> • <%= WebUtil.escapeHtml(item.getAppointmentMode().getDisplayName()) %></span></div>
                        <div class="appointment-row__time"><strong><%= item.getAppointmentTime().format(displayTime) %></strong><span><%= WebUtil.escapeHtml(item.getAppointmentNumber()) %></span></div>
                    </a>
                <% } %>
            </div>
        <% } %>
    </article>

    <article class="card quick-card">
        <div class="card__header"><div><p class="eyebrow">SHORTCUTS</p><h2>Quick actions</h2></div></div>
        <a class="quick-action" href="<%= contextPath %>/appointments/new"><span class="quick-action__icon orange">＋</span><span><strong>New appointment</strong><small>Add a patient visit</small></span><b>›</b></a>
        <a class="quick-action" href="<%= contextPath %>/appointments/search"><span class="quick-action__icon teal">⌕</span><span><strong>Search records</strong><small>Find by appointment no.</small></span><b>›</b></a>
        <a class="quick-action" href="<%= contextPath %>/bill"><span class="quick-action__icon blue">₨</span><span><strong>Create a bill</strong><small>Calculate treatment fees</small></span><b>›</b></a>
        <a class="quick-action" href="<%= contextPath %>/help"><span class="quick-action__icon violet">?</span><span><strong>Staff help</strong><small>Read the step-by-step guide</small></span><b>›</b></a>
    </article>
</section>
<%@ include file="../jspf/app-end.jspf" %>
