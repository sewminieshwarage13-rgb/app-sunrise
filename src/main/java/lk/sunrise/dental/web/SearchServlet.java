package lk.sunrise.dental.web;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import lk.sunrise.dental.store.AppointmentStore;

import java.io.IOException;

@WebServlet("/appointments/search")
public final class SearchServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        String number = WebUtil.clean(request.getParameter("number")).toUpperCase();
        if (!number.isBlank()) {
            request.setAttribute("searched", true);
            request.setAttribute("number", number);
            store(request).findByNumber(number).ifPresentOrElse(
                    appointment -> request.setAttribute("appointment", appointment),
                    () -> request.setAttribute("notFound", true));
        }
        request.getRequestDispatcher("/WEB-INF/views/search.jsp").forward(request, response);
    }

    private AppointmentStore store(HttpServletRequest request) {
        return (AppointmentStore) request.getServletContext().getAttribute("appointmentStore");
    }
}
