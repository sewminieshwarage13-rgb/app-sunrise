package lk.sunrise.dental.web;

import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.store.AppointmentStore;

import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

/**
 * Secured REST-style endpoint that exposes one appointment record as JSON.
 * Example: GET /sunrise/api/appointments/APT-1001
 */
@WebServlet("/api/appointments/*")
public final class AppointmentApiServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String pathInfo = request.getPathInfo();
        if (pathInfo == null || pathInfo.length() <= 1 || pathInfo.indexOf('/', 1) >= 0) {
            writeJson(response, HttpServletResponse.SC_BAD_REQUEST,
                    "{\"error\":\"Provide an appointment number in the URL.\"}");
            return;
        }

        String appointmentNumber = URLDecoder.decode(pathInfo.substring(1), StandardCharsets.UTF_8).trim();
        AppointmentStore store = (AppointmentStore) request.getServletContext().getAttribute("appointmentStore");
        var appointment = store.findByNumber(appointmentNumber);
        if (appointment.isEmpty()) {
            writeJson(response, HttpServletResponse.SC_NOT_FOUND,
                    "{\"error\":\"Appointment not found.\"}");
            return;
        }
        writeJson(response, HttpServletResponse.SC_OK, toJson(appointment.get()));
    }

    private String toJson(Appointment appointment) {
        return "{" +
                "\"appointmentNumber\":\"" + escape(appointment.getAppointmentNumber()) + "\"," +
                "\"patientName\":\"" + escape(appointment.getPatientName()) + "\"," +
                "\"contactNumber\":\"" + escape(appointment.getContactNumber()) + "\"," +
                "\"dentistName\":\"" + escape(appointment.getDentistName()) + "\"," +
                "\"treatmentType\":\"" + escape(appointment.getTreatmentType()) + "\"," +
                "\"appointmentMode\":\"" + escape(appointment.getAppointmentMode().name()) + "\"," +
                "\"appointmentDate\":\"" + appointment.getAppointmentDate() + "\"," +
                "\"appointmentTime\":\"" + appointment.getAppointmentTime() + "\"}";
    }

    private String escape(String value) {
        return value.replace("\\", "\\\\")
                .replace("\"", "\\\"")
                .replace("\n", "\\n")
                .replace("\r", "\\r");
    }

    private void writeJson(HttpServletResponse response, int status, String content) throws IOException {
        response.setStatus(status);
        response.setContentType("application/json;charset=UTF-8");
        response.getWriter().write(content);
    }
}
