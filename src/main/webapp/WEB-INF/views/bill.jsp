<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" language="java" %>
<%@ page import="java.math.BigDecimal,java.time.LocalDate,java.time.format.DateTimeFormatter,lk.sunrise.dental.model.Appointment,lk.sunrise.dental.web.WebUtil" %>
<% request.setAttribute("pageTitle", "Calculate & Print Bill"); %>
<%@ include file="../jspf/app-start.jspf" %>
<%
    Appointment billAppointment = (Appointment) request.getAttribute("appointment");
    DateTimeFormatter billDateFormat = DateTimeFormatter.ofPattern("dd MMM yyyy");
%>
<section class="bill-search no-print">
    <div><p class="eyebrow">PATIENT BILLING</p><h2>Generate a treatment receipt</h2><p>Find an appointment to calculate the consultation and treatment charges.</p></div>
    <form class="search-box" action="<%= contextPath %>/bill" method="get">
        <label class="sr-only" for="bill-search">Appointment number</label>
        <span>₨</span><input id="bill-search" type="text" name="number" required placeholder="e.g. APT-1001" value="<%= WebUtil.escapeHtml((String) request.getAttribute("number")) %>">
        <button class="button button--primary" type="submit">Calculate bill</button>
    </form>
</section>

<% if (request.getAttribute("notFound") != null) { %>
    <section class="card empty-state"><span>₨</span><h2>Cannot create this bill</h2><p>No record matches “<strong><%= WebUtil.escapeHtml((String) request.getAttribute("number")) %></strong>”.</p></section>
<% } else if (billAppointment != null) { %>
    <section class="receipt-wrap">
        <article class="receipt">
            <header class="receipt__header">
                <div class="brand brand--receipt"><span class="brand__mark">S+</span><span><strong>Sunrise</strong><small>Dental Clinic</small></span></div>
                <div><span>OFFICIAL RECEIPT</span><strong>INV-<%= WebUtil.escapeHtml(billAppointment.getAppointmentNumber().substring(4)) %></strong></div>
            </header>
            <div class="receipt__meta">
                <div><small>Billed to</small><strong><%= WebUtil.escapeHtml(billAppointment.getPatientName()) %></strong><span><%= WebUtil.escapeHtml(billAppointment.getContactNumber()) %></span></div>
                <div><small>Receipt date</small><strong><%= ((LocalDate) request.getAttribute("invoiceDate")).format(billDateFormat) %></strong><span>Appointment: <%= WebUtil.escapeHtml(billAppointment.getAppointmentNumber()) %></span></div>
            </div>
            <div class="receipt__appointment">
                <span><small>Dentist</small><strong><%= WebUtil.escapeHtml(billAppointment.getDentistName()) %></strong></span>
                <span><small>Visit date</small><strong><%= billAppointment.getAppointmentDate().format(billDateFormat) %> at <%= billAppointment.getAppointmentTime() %></strong></span>
                <span><small>Appointment method</small><strong><%= WebUtil.escapeHtml(billAppointment.getAppointmentMode().getDisplayName()) %></strong></span>
            </div>
            <table class="bill-table">
                <thead><tr><th>Description</th><th>Amount (LKR)</th></tr></thead>
                <tbody>
                    <tr><td><strong>Consultation fee</strong><span>Standard dental consultation</span></td><td>Rs. <%= String.format("%,.2f", (BigDecimal) request.getAttribute("consultationFee")) %></td></tr>
                    <tr><td><strong><%= WebUtil.escapeHtml(billAppointment.getTreatmentType()) %></strong><span>Treatment charge</span></td><td>Rs. <%= String.format("%,.2f", (BigDecimal) request.getAttribute("treatmentFee")) %></td></tr>
                </tbody>
                <tfoot><tr><td>Total payable</td><td>Rs. <%= String.format("%,.2f", (BigDecimal) request.getAttribute("total")) %></td></tr></tfoot>
            </table>
            <div class="receipt__note"><span>✓</span><p><strong>Thank you for choosing Sunrise Dental Clinic.</strong><br>Please retain this receipt for your records.</p></div>
            <footer class="receipt__footer"><span>Colombo, Sri Lanka</span><span>011 234 5678</span><span>care@sunrisedental.lk</span></footer>
        </article>
        <div class="receipt-actions no-print">
            <a class="button button--secondary" href="<%= contextPath %>/bill">Create another bill</a>
            <button class="button button--primary" type="button" onclick="window.print()">Print receipt</button>
        </div>
    </section>
<% } else { %>
    <section class="card empty-state billing-empty"><span>₨</span><h2>Ready to calculate</h2><p>Enter an appointment number above. Treatment pricing and the standard consultation fee will be added automatically.</p></section>
<% } %>
<%@ include file="../jspf/app-end.jspf" %>
