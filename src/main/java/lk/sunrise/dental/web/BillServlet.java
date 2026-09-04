package lk.sunrise.dental.web;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.service.TreatmentCatalog;
import lk.sunrise.dental.store.AppointmentStore;

import java.io.IOException;
import java.time.LocalDate;
import java.util.Optional;

@WebServlet("/bill")
public final class BillServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String number = WebUtil.clean(request.getParameter("number")).toUpperCase();
        if (!number.isBlank()) {
            request.setAttribute("searched", true);
            request.setAttribute("number", number);
            Optional<Appointment> appointment = store(request).findByNumber(number);
            if (appointment.isPresent()) {
                Appointment item = appointment.get();
                request.setAttribute("appointment", item);
                request.setAttribute("consultationFee", TreatmentCatalog.CONSULTATION_FEE);
                request.setAttribute("treatmentFee", TreatmentCatalog.treatmentFee(item.getTreatmentType()));
                request.setAttribute("total", TreatmentCatalog.totalFor(item.getTreatmentType()));
                request.setAttribute("invoiceDate", LocalDate.now());
            } else {
                request.setAttribute("notFound", true);
            }
        }
        request.getRequestDispatcher("/WEB-INF/views/bill.jsp").forward(request, response);
    }

    private AppointmentStore store(HttpServletRequest request) {
        return (AppointmentStore) request.getServletContext().getAttribute("appointmentStore");
    }
}
