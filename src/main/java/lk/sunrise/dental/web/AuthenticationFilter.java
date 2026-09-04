package lk.sunrise.dental.web;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import java.io.IOException;

@WebFilter("/*")
public final class AuthenticationFilter implements Filter {
    @Override
    public void init(FilterConfig filterConfig) {
        // No filter configuration is required.
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        String path = httpRequest.getRequestURI().substring(httpRequest.getContextPath().length());
        HttpSession session = httpRequest.getSession(false);

        boolean publicPath = path.equals("/") || path.equals("/login")
                || path.startsWith("/assets/");
        boolean authenticated = session != null && session.getAttribute("user") != null;

        if (publicPath || authenticated) {
            chain.doFilter(request, response);
            return;
        }
        httpResponse.sendRedirect(httpRequest.getContextPath() + "/login?expired=1");
    }

    @Override
    public void destroy() {
        // No resources need to be released.
    }
}
