package lk.sunrise.dental.service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public final class AuthService {
    public static final String DEMO_USERNAME = "admin";
    private static final byte[] PASSWORD_HASH = hexToBytes(
            "91ab58989f15367fbee1505dfb7c8cfdd78a99774757717e71b9c6044c358bf1");

    public boolean authenticate(String username, String password) {
        if (!DEMO_USERNAME.equals(username) || password == null) {
            return false;
        }
        return MessageDigest.isEqual(PASSWORD_HASH, sha256(password));
    }

    private static byte[] sha256(String value) {
        try {
            return MessageDigest.getInstance("SHA-256")
                    .digest(value.getBytes(StandardCharsets.UTF_8));
        } catch (NoSuchAlgorithmException exception) {
            throw new IllegalStateException("SHA-256 is unavailable", exception);
        }
    }

    private static byte[] hexToBytes(String value) {
        byte[] result = new byte[value.length() / 2];
        for (int index = 0; index < value.length(); index += 2) {
            result[index / 2] = (byte) Integer.parseInt(value.substring(index, index + 2), 16);
        }
        return result;
    }
}
