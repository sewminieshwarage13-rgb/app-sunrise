package lk.sunrise.dental.store;

import com.mysql.cj.jdbc.MysqlDataSource;

import javax.sql.DataSource;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

/** Creates the application's MySQL data source from tracked and local properties. */
public final class DatabaseConfiguration {
    private static final String CONFIGURATION_RESOURCE = "database.properties";
    private static final String LOCAL_CONFIGURATION_RESOURCE = "database.local.properties";

    private DatabaseConfiguration() {
    }

    public static DataSource createDataSource() {
        Properties properties = loadProperties();
        MysqlDataSource dataSource = new MysqlDataSource();
        dataSource.setURL(setting(properties, "sunrise.db.url", "db.url"));
        dataSource.setUser(setting(properties, "sunrise.db.username", "db.username"));
        dataSource.setPassword(setting(properties, "sunrise.db.password", "db.password"));
        return dataSource;
    }

    private static Properties loadProperties() {
        Properties properties = new Properties();
        try (InputStream stream = DatabaseConfiguration.class.getClassLoader()
                .getResourceAsStream(CONFIGURATION_RESOURCE)) {
            if (stream == null) {
                throw new IllegalStateException("The MySQL configuration file is missing.");
            }
            properties.load(stream);
            loadLocalOverrides(properties);
            return properties;
        } catch (IOException exception) {
            throw new IllegalStateException("Unable to read the MySQL configuration.", exception);
        }
    }

    private static void loadLocalOverrides(Properties properties) throws IOException {
        try (InputStream stream = DatabaseConfiguration.class.getClassLoader()
                .getResourceAsStream(LOCAL_CONFIGURATION_RESOURCE)) {
            if (stream != null) {
                properties.load(stream);
            }
        }
    }

    private static String setting(Properties properties, String systemProperty, String propertyName) {
        String value = System.getProperty(systemProperty);
        if (value == null || value.isBlank()) {
            value = properties.getProperty(propertyName);
        }
        if (value == null || value.isBlank()) {
            throw new IllegalStateException("Missing MySQL setting: " + propertyName);
        }
        return value.trim();
    }
}
