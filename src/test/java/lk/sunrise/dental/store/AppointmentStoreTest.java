package lk.sunrise.dental.store;

import lk.sunrise.dental.model.Appointment;
import lk.sunrise.dental.model.AppointmentMode;
import org.h2.jdbcx.JdbcDataSource;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.sql.Connection;
import java.sql.Statement;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AppointmentStoreTest {
    private AppointmentStore store;

    @BeforeEach
    void setUpDatabase() throws Exception {
        JdbcDataSource dataSource = new JdbcDataSource();
        dataSource.setURL("jdbc:h2:mem:appointments_" + UUID.randomUUID() + ";MODE=MySQL;DB_CLOSE_DELAY=-1");
        try (Connection connection = dataSource.getConnection(); Statement statement = connection.createStatement()) {
            statement.execute("""
                    CREATE TABLE appointments (
                        id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        appointment_number VARCHAR(20) NOT NULL UNIQUE,
                        patient_name VARCHAR(100) NOT NULL,
                        address VARCHAR(255) NOT NULL,
                        contact_number VARCHAR(20) NOT NULL,
                        dentist_name VARCHAR(100) NOT NULL,
                        treatment_type VARCHAR(100) NOT NULL,
                        appointment_mode VARCHAR(16) NOT NULL,
                        appointment_date DATE NOT NULL,
                        appointment_time TIME NOT NULL,
                        CONSTRAINT uq_dentist_appointment_slot
                            UNIQUE (dentist_name, appointment_date, appointment_time)
                    )
                    """);
        }
        store = new AppointmentStore(dataSource);
    }

    @Test
    void savesAndFindsAppointmentInMySql() throws Exception {
        store.save(appointment("APT-1001", "Dr. Amaya Perera", LocalTime.of(9, 0)));

        assertTrue(store.findByNumber("apt-1001").isPresent());
        assertEquals("Asha Silva", store.findByNumber("APT-1001").orElseThrow().getPatientName());
        assertEquals(AppointmentMode.PHYSICAL,
                store.findByNumber("APT-1001").orElseThrow().getAppointmentMode());
        assertEquals(1, store.findAll().size());
    }

    @Test
    void storesOnlineAppointmentMethod() throws Exception {
        store.save(appointment("APT-1008", "Dr. Shanika Silva", LocalTime.of(11, 0), AppointmentMode.ONLINE));

        assertEquals(AppointmentMode.ONLINE,
                store.findByNumber("APT-1008").orElseThrow().getAppointmentMode());
    }

    @Test
    void rejectsDuplicateAppointmentNumber() throws Exception {
        store.save(appointment("APT-1001", "Dr. Amaya Perera", LocalTime.of(9, 0)));

        assertThrows(DuplicateAppointmentException.class,
                () -> store.save(appointment("APT-1001", "Dr. Nimal Fernando", LocalTime.of(10, 0))));
    }

    @Test
    void preventsDentistDoubleBooking() throws Exception {
        store.save(appointment("APT-1001", "Dr. Amaya Perera", LocalTime.of(9, 0)));

        DuplicateAppointmentException error = assertThrows(DuplicateAppointmentException.class,
                () -> store.save(appointment("APT-1002", "Dr. Amaya Perera", LocalTime.of(9, 0))));
        assertTrue(error.getMessage().contains("already booked"));
    }

    @Test
    void generatesNextAppointmentNumber() throws Exception {
        assertEquals("APT-1001", store.nextAppointmentNumber());
        store.save(appointment("APT-1007", "Dr. Amaya Perera", LocalTime.of(9, 0)));
        assertEquals("APT-1008", store.nextAppointmentNumber());
    }

    private Appointment appointment(String number, String dentist, LocalTime time) {
        return appointment(number, dentist, time, AppointmentMode.PHYSICAL);
    }

    private Appointment appointment(String number, String dentist, LocalTime time, AppointmentMode mode) {
        return new Appointment(number, "Asha Silva", "12 Palm Road, Colombo",
                "0771234567", dentist, "Teeth Cleaning",
                mode, LocalDate.now().plusDays(2), time);
    }
}
