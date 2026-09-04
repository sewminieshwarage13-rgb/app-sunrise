package lk.sunrise.dental.web;

import com.mysql.cj.jdbc.AbandonedConnectionCleanupThread;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;
import javax.servlet.annotation.WebListener;
import javax.sql.DataSource;
import lk.sunrise.dental.store.AppointmentStore;
import lk.sunrise.dental.store.DatabaseConfiguration;

import java.sql.Connection;
import java.sql.SQLException;

@WebListener
public final class ClinicContextListener implements ServletContextListener {
    @Override
    public void contextInitialized(ServletContextEvent event) {
        DataSource dataSource = DatabaseConfiguration.createDataSource();
        try (Connection ignored = dataSource.getConnection()) {
            event.getServletContext().setAttribute("appointmentStore", new AppointmentStore(dataSource));
        } catch (SQLException exception) {
            throw new IllegalStateException("Unable to connect to the Sunrise MySQL database.", exception);
        }
    }

    @Override
    public void contextDestroyed(ServletContextEvent event) {
        // Stop MySQL Connector/J's cleanup thread before Tomcat unloads this webapp.
        AbandonedConnectionCleanupThread.checkedShutdown();
    }
}
