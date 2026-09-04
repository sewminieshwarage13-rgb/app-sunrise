package lk.sunrise.dental.web;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.model.AppointmentMode;
import lk.sunrise.dental.service.AppointmentValidator;
import lk.sunrise.dental.service.TreatmentCatalog;
import lk.sunrise.dental.store.AppointmentStore;
import lk.sunrise.dental.store.DuplicateAppointmentException;

import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.time.DateTimeException;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.Map;

@WebServlet("/appointments/new")
public final class AppointmentServlet extends HttpServlet {
    private static final String[] DENTISTS = {
            "Dr. Amaya Perera", "Dr. Nimal Fernando", "Dr. Shanika Silva"
    };
    private final AppointmentValidator validator = new AppointmentValidator();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        prepareForm(request);
        request.setAttribute("appointmentNumber", store(request).nextAppointmentNumber());
        request.getRequestDispatcher("/WEB-INF/views/appointment-form.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");
        copyFormValues(request);
        prepareForm(request);

        Appointment appointment;
        try {
            appointment = new Appointment(
                    WebUtil.clean(request.getParameter("appointmentNumber")).toUpperCase(),
                    WebUtil.clean(request.getParameter("patientName")),
                    WebUtil.clean(request.getParameter("address")),
                    WebUtil.clean(request.getParameter("contactNumber")),
                    WebUtil.clean(request.getParameter("dentistName")),
                    WebUtil.clean(request.getParameter("treatmentType")),
                    AppointmentMode.fromValue(WebUtil.clean(request.getParameter("appointmentMode"))),
                    LocalDate.parse(WebUtil.clean(request.getParameter("appointmentDate"))),
                    LocalTime.parse(WebUtil.clean(request.getParameter("appointmentTime"))));
        } catch (DateTimeException | IllegalArgumentException exception) {
            request.setAttribute("formError", "Enter a valid appointment date, time and visit method.");
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            request.getRequestDispatcher("/WEB-INF/views/appointment-form.jsp").forward(request, response);
            return;
        }

        Map<String, String> errors = validator.validate(appointment);
        if (!errors.isEmpty()) {
            request.setAttribute("errors", errors);
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            request.getRequestDispatcher("/WEB-INF/views/appointment-form.jsp").forward(request, response);
            return;
        }

        try {
            store(request).save(appointment);
        } catch (DuplicateAppointmentException exception) {
            request.setAttribute("formError", exception.getMessage());
            response.setStatus(HttpServletResponse.SC_CONFLICT);
            request.getRequestDispatcher("/WEB-INF/views/appointment-form.jsp").forward(request, response);
            return;
        }

        String number = URLEncoder.encode(appointment.getAppointmentNumber(), StandardCharsets.UTF_8);
        response.sendRedirect(request.getContextPath() + "/appointments/search?number=" + number + "&created=1");
    }

    private void prepareForm(HttpServletRequest request) {
        request.setAttribute("dentists", DENTISTS);
        request.setAttribute("treatments", TreatmentCatalog.treatmentTypes());
        request.setAttribute("appointmentModes", AppointmentMode.values());
        request.setAttribute("today", LocalDate.now().toString());
    }

    private void copyFormValues(HttpServletRequest request) {
        String[] fields = {"appointmentNumber", "patientName", "address", "contactNumber",
                "dentistName", "treatmentType", "appointmentMode", "appointmentDate", "appointmentTime"};
        for (String field : fields) {
            request.setAttribute(field, WebUtil.clean(request.getParameter(field)));
        }
    }

    private AppointmentStore store(HttpServletRequest request) {
        return (AppointmentStore) request.getServletContext().getAttribute("appointmentStore");
    }
}
