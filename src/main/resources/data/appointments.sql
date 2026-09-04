-- ============================================
-- Dental Appointments: Table + Seed Data
-- ============================================

CREATE DATABASE IF NOT EXISTS dental_clinic;
USE dental_clinic;

DROP TABLE IF EXISTS appointments;

CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_number VARCHAR(20) NOT NULL UNIQUE,
    patient_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    contact_number VARCHAR(20) NOT NULL,
    dentist_name VARCHAR(100) NOT NULL,
    treatment_type VARCHAR(100) NOT NULL,
    appointment_mode ENUM('PHYSICAL', 'ONLINE') NOT NULL DEFAULT 'PHYSICAL',
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT uq_dentist_appointment_slot
        UNIQUE (dentist_name, appointment_date, appointment_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO appointments
    (appointment_number, patient_name, address, contact_number, dentist_name, treatment_type, appointment_mode, appointment_date, appointment_time)
VALUES
    ('APT-1001', 'Nethmi Jayasinghe', '45 Flower Road, Colombo 07', '0771234567', 'Dr. Amaya Perera', 'Dental Filling', 'PHYSICAL', '2026-08-20', '10:30:00'),
    ('APT-1002', 'Sanduni Perera', '28 Galle Road, Dehiwala', '0714567890', 'Dr. Nimal Fernando', 'Teeth Cleaning', 'ONLINE', '2026-08-20', '11:15:00'),
    ('APT-1003', 'Kasun Fernando', '18 Lake Drive, Colombo 05', '0719876543', 'Dr. Shanika Silva', 'Root Canal Treatment', 'PHYSICAL', '2026-08-21', '09:00:00'),
    ('APT-1004', 'Dilshan Silva', '72 Temple Lane, Nugegoda', '0763456789', 'Dr. Amaya Perera', 'Tooth Extraction', 'PHYSICAL', '2026-08-22', '14:30:00'),
    ('APT-1005', 'Ishara Wickramasinghe', '9 Park Avenue, Rajagiriya', '0752345678', 'Dr. Nimal Fernando', 'Teeth Whitening', 'ONLINE', '2026-08-24', '16:00:00');

-- Quick check
-- SELECT * FROM appointments ORDER BY appointment_date, appointment_time;
