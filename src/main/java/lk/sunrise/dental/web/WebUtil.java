package lk.sunrise.dental.web;

public final class WebUtil {
    private WebUtil() { }

    public static String clean(String value) {
        return value == null ? "" : value.trim();
    }

    public static String escapeHtml(String value) {
        if (value == null) {
            return "";
        }
        return value.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace("\"", "&quot;")
                .replace("'", "&#39;");
    }
}
