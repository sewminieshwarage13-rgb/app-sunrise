package lk.sunrise.dental.service;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class AuthServiceTest {
    private final AuthService authService = new AuthService();

    @Test
    void acceptsAuthorizedStaffCredentials() {
        assertTrue(authService.authenticate("admin", "Sunrise@123"));
    }

    @Test
    void rejectsIncorrectPassword() {
        assertFalse(authService.authenticate("admin", "wrong-password"));
    }

    @Test
    void rejectsUnknownUsername() {
        assertFalse(authService.authenticate("visitor", "Sunrise@123"));
    }
}

