"""
Keep-Alive Component for Streamlit
Prevents Streamlit Cloud from putting the app to sleep due to inactivity.

This works by injecting a hidden JavaScript component that sends periodic
activity signals to keep the WebSocket connection alive.
"""

import streamlit as st
import streamlit.components.v1 as components


def inject_keep_alive(interval_seconds: int = 300):
    """
    Inject a JavaScript keep-alive mechanism to prevent Streamlit idle timeout.

    Args:
        interval_seconds: How often to send keep-alive signals (default: 5 minutes)

    Note:
        - Streamlit Cloud typically puts apps to sleep after 15-30 minutes of inactivity
        - This component sends periodic signals to maintain the WebSocket connection
        - The component is invisible and doesn't affect the UI
    """

    # JavaScript that sends periodic activity signals
    keep_alive_js = f"""
    <script>
    (function() {{
        // Configuration
        const INTERVAL_MS = {interval_seconds * 1000};
        const COMPONENT_ID = 'streamlit-keep-alive';

        // Prevent multiple instances
        if (window._streamlitKeepAliveActive) {{
            return;
        }}
        window._streamlitKeepAliveActive = true;

        // Keep-alive function
        function sendKeepAlive() {{
            try {{
                // Method 1: Trigger a minimal DOM interaction
                const event = new Event('mousemove', {{ bubbles: true }});
                document.dispatchEvent(event);

                // Method 2: Access Streamlit's internal connection
                if (window.parent && window.parent.streamlitApp) {{
                    // This triggers Streamlit to recognize activity
                    console.log('[Keep-Alive] Signal sent at ' + new Date().toISOString());
                }}

                // Method 3: Touch the iframe container to maintain connection
                const iframes = window.parent.document.querySelectorAll('iframe');
                iframes.forEach(function(iframe) {{
                    if (iframe.contentWindow === window) {{
                        iframe.style.opacity = iframe.style.opacity === '1' ? '0.9999' : '1';
                    }}
                }});

            }} catch (e) {{
                // Silently handle cross-origin errors
            }}
        }}

        // Start the keep-alive interval
        setInterval(sendKeepAlive, INTERVAL_MS);

        // Send initial signal
        sendKeepAlive();

        console.log('[Keep-Alive] Initialized with ' + ({interval_seconds}) + 's interval');
    }})();
    </script>
    <div id="streamlit-keep-alive" style="display:none;"></div>
    """

    # Inject the component (height=0 makes it invisible)
    components.html(keep_alive_js, height=0, width=0)


def inject_auto_refresh(interval_minutes: int = 10):
    """
    Alternative approach: Auto-refresh the page periodically.
    Use this if keep_alive doesn't work for your deployment.

    Warning: This will cause a full page reload, which may interrupt user activity.
    Only use this as a last resort.

    Args:
        interval_minutes: How often to refresh the page (default: 10 minutes)
    """

    auto_refresh_js = f"""
    <script>
    (function() {{
        const INTERVAL_MS = {interval_minutes * 60 * 1000};
        const ACTIVITY_THRESHOLD_MS = {(interval_minutes - 1) * 60 * 1000};

        // Track last user activity
        let lastActivity = Date.now();

        function updateActivity() {{
            lastActivity = Date.now();
        }}

        // Listen for user activity
        document.addEventListener('click', updateActivity);
        document.addEventListener('keydown', updateActivity);
        document.addEventListener('mousemove', updateActivity);
        document.addEventListener('scroll', updateActivity);

        // Check if we need to refresh
        function checkRefresh() {{
            const timeSinceActivity = Date.now() - lastActivity;

            // Only refresh if user has been inactive
            if (timeSinceActivity > ACTIVITY_THRESHOLD_MS) {{
                console.log('[Auto-Refresh] Refreshing page to maintain session...');
                window.parent.location.reload();
            }}
        }}

        // Check periodically
        setInterval(checkRefresh, INTERVAL_MS);

        console.log('[Auto-Refresh] Initialized with ' + {interval_minutes} + ' minute interval');
    }})();
    </script>
    """

    components.html(auto_refresh_js, height=0, width=0)


def show_activity_indicator():
    """
    Optional: Show a small indicator that the keep-alive is active.
    Useful for debugging.
    """

    indicator_html = """
    <div style="
        position: fixed;
        bottom: 10px;
        right: 10px;
        padding: 5px 10px;
        background: rgba(0, 128, 0, 0.1);
        border: 1px solid rgba(0, 128, 0, 0.3);
        border-radius: 5px;
        font-size: 10px;
        color: #006400;
        z-index: 9999;
    ">
        <span id="keep-alive-indicator">🟢 Session active</span>
    </div>
    <script>
    (function() {
        const indicator = document.getElementById('keep-alive-indicator');
        let dots = 0;

        setInterval(function() {
            dots = (dots + 1) % 4;
            const dotStr = '.'.repeat(dots);
            indicator.textContent = '🟢 Session active' + dotStr;
        }, 1000);
    })();
    </script>
    """

    components.html(indicator_html, height=50)
