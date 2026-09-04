package lk.sunrise.dental.store;

import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.model.AppointmentMode;

import javax.sql.DataSource;
import java.io.IOException;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLIntegrityConstraintViolationException;
import java.sql.Time;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.regex.Pattern;

/** MySQL-backed repository for clinic appointments. */
public final class AppointmentStore {
    private static final Pattern APPOINTMENT_NUMBER_PATTERN = Pattern.compile("APT-(\\d+)");
    private final DataSource dataSource;

    public AppointmentStore(DataSource dataSource) {
        this.dataSource = Objects.requireNonNull(dataSource);
    }

    public void save(Appointment appointment) throws IOException, DuplicateAppointmentException {
        try (Connection connection = dataSource.getConnection()) {
            if (appointmentNumberExists(connection, appointment.getAppointmentNumber())) {
                throw new DuplicateAppointmentException("That appointment number already exists.");
            }
            if (dentistSlotExists(connection, appointment)) {
                throw new DuplicateAppointmentException("The selected dentist is already booked at that time.");
            }

            try (PreparedStatement statement = connection.prepareStatement("""
                    INSERT INTO appointments
                        (appointment_number, patient_name, address, contact_number, dentist_name,
                         treatment_type, appointment_mode, appointment_date, appointment_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """)) {
                statement.setString(1, appointment.getAppointmentNumber());
                statement.setString(2, appointment.getPatientName());
                statement.setString(3, appointment.getAddress());
                statement.setString(4, appointment.getContactNumber());
                statement.setString(5, appointment.getDentistName());
                statement.setString(6, appointment.getTreatmentType());
                statement.setString(7, appointment.getAppointmentMode().name());
                statement.setDate(8, Date.valueOf(appointment.getAppointmentDate()));
                statement.setTime(9, Time.valueOf(appointment.getAppointmentTime()));
                statement.executeUpdate();
            }
        } catch (SQLIntegrityConstraintViolationException exception) {
            throw duplicateException(exception);
        } catch (SQLException exception) {
            throw databaseFailure("save the appointment", exception);
        }
    }

    public Optional<Appointment> findByNumber(String appointmentNumber) throws IOException {
        if (appointmentNumber == null || appointmentNumber.isBlank()) {
            return Optional.empty();
        }

        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement("""
                     SELECT appointment_number, patient_name, address, contact_number, dentist_name,
                            treatment_type, appointment_mode, appointment_date, appointment_time
                     FROM appointments
                     WHERE UPPER(appointment_number) = UPPER(?)
                     """)) {
            statement.setString(1, appointmentNumber.trim());
            try (ResultSet results = statement.executeQuery()) {
                return results.next() ? Optional.of(toAppointment(results)) : Optional.empty();
            }
        } catch (SQLException exception) {
            throw databaseFailure("find the appointment", exception);
        }
    }

    public List<Appointment> findAll() throws IOException {
        return queryAppointments("""
                SELECT appointment_number, patient_name, address, contact_number, dentist_name,
                       treatment_type, appointment_mode, appointment_date, appointment_time
                FROM appointments
                ORDER BY appointment_date, appointment_time, appointment_number
                """);
    }

    public List<Appointment> upcoming(int limit) throws IOException {
        if (limit <= 0) {
            return List.of();
        }

        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement("""
                     SELECT appointment_number, patient_name, address, contact_number, dentist_name,
                            treatment_type, appointment_mode, appointment_date, appointment_time
                     FROM appointments
                     WHERE appointment_date >= ?
                     ORDER BY appointment_date, appointment_time, appointment_number
                     LIMIT ?
                     """)) {
            statement.setDate(1, Date.valueOf(LocalDate.now()));
            statement.setInt(2, limit);
            return readAppointments(statement);
        } catch (SQLException exception) {
            throw databaseFailure("load upcoming appointments", exception);
        }
    }

    public long countForDate(LocalDate date) throws IOException {
        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(
                     "SELECT COUNT(*) FROM appointments WHERE appointment_date = ?")) {
            statement.setDate(1, Date.valueOf(date));
            try (ResultSet results = statement.executeQuery()) {
                results.next();
                return results.getLong(1);
            }
        } catch (SQLException exception) {
            throw databaseFailure("count appointments", exception);
        }
    }

    public String nextAppointmentNumber() throws IOException {
        int highest = 1000;
        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(
                     "SELECT appointment_number FROM appointments WHERE appointment_number LIKE 'APT-%'");
             ResultSet results = statement.executeQuery()) {
            while (results.next()) {
                var matcher = APPOINTMENT_NUMBER_PATTERN.matcher(results.getString(1));
                if (matcher.matches()) {
                    highest = Math.max(highest, Integer.parseInt(matcher.group(1)));
                }
            }
            return "APT-" + (highest + 1);
        } catch (SQLException exception) {
            throw databaseFailure("generate the next appointment number", exception);
        }
    }

    private List<Appointment> queryAppointments(String sql) throws IOException {
        try (Connection connection = dataSource.getConnection();
             PreparedStatement statement = connection.prepareStatement(sql)) {
            return readAppointments(statement);
        } catch (SQLException exception) {
            throw databaseFailure("load appointments", exception);
        }
    }

    private List<Appointment> readAppointments(PreparedStatement statement) throws SQLException {
        try (ResultSet results = statement.executeQuery()) {
            List<Appointment> appointments = new ArrayList<>();
            while (results.next()) {
                appointments.add(toAppointment(results));
            }
            return appointments;
        }
    }

    private boolean appointmentNumberExists(Connection connection, String appointmentNumber) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement(
                "SELECT 1 FROM appointments WHERE UPPER(appointment_number) = UPPER(?)")) {
            statement.setString(1, appointmentNumber);
            try (ResultSet results = statement.executeQuery()) {
                return results.next();
            }
        }
    }

    private boolean dentistSlotExists(Connection connection, Appointment appointment) throws SQLException {
        try (PreparedStatement statement = connection.prepareStatement("""
                SELECT 1 FROM appointments
                WHERE dentist_name = ? AND appointment_date = ? AND appointment_time = ?
                """)) {
            statement.setString(1, appointment.getDentistName());
            statement.setDate(2, Date.valueOf(appointment.getAppointmentDate()));
            statement.setTime(3, Time.valueOf(appointment.getAppointmentTime()));
            try (ResultSet results = statement.executeQuery()) {
                return results.next();
            }
        }
    }

    private Appointment toAppointment(ResultSet results) throws SQLException {
        return new Appointment(
                results.getString("appointment_number"),
                results.getString("patient_name"),
                results.getString("address"),
                results.getString("contact_number"),
                results.getString("dentist_name"),
                results.getString("treatment_type"),
                AppointmentMode.fromValue(results.getString("appointment_mode")),
                results.getDate("appointment_date").toLocalDate(),
                results.getTime("appointment_time").toLocalTime());
    }

    private DuplicateAppointmentException duplicateException(SQLIntegrityConstraintViolationException exception) {
        String message = exception.getMessage();
        if (message != null && message.contains("uq_dentist_appointment_slot")) {
            return new DuplicateAppointmentException("The selected dentist is already booked at that time.");
        }
        return new DuplicateAppointmentException("That appointment number already exists.");
    }

    private IOException databaseFailure(String action, SQLException exception) {
        return new IOException("Unable to " + action + " in MySQL.", exception);
    }
}
