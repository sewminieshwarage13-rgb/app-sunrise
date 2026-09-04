package lk.sunrise.dental.web;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lk.sunrise.dental.store.AppointmentStore;

import java.io.IOException;
import java.time.LocalDate;

@WebServlet("/dashboard")
public final class DashboardServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        AppointmentStore store = store(request);
        request.setAttribute("todayCount", store.countForDate(LocalDate.now()));
        request.setAttribute("totalCount", store.findAll().size());
        request.setAttribute("upcoming", store.upcoming(5));
        request.setAttribute("nextNumber", store.nextAppointmentNumber());
        request.getRequestDispatcher("/WEB-INF/views/dashboard.jsp").forward(request, response);
    }

    private AppointmentStore store(HttpServletRequest request) {
        return (AppointmentStore) request.getServletContext().getAttribute("appointmentStore");
    }
}
