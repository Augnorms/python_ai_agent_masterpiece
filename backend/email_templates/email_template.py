def generate_email_body(flow, tds, quality, report_text):
    """Generates a styled HTML email body based on the agent's report."""
    
    # Choose a color based on the quality status
    status_color = "#10b981" # Green (Excellent/Good)
    if quality == "Warning":
        status_color = "#f59e0b" # Orange
    elif quality == "Poor":
        status_color = "#ef4444" # Red

    # Convert newlines in the agent's report to HTML line breaks
    formatted_report = report_text.replace("\n", "<br>")

    body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #f8fafc; padding: 20px; border-radius: 8px;">
        <div style="background-color: #0f172a; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
            <h1 style="margin: 0; font-size: 24px;">🌊 Northstar Plant Diagnostic</h1>
            <p style="margin: 5px 0 0 0; color: #94a3b8;">Autonomous AI Supervisor Report</p>
        </div>
        
        <div style="background-color: white; padding: 20px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px;">
            <h2 style="color: #1e293b; margin-top: 0;">Live Telemetry Snapshot</h2>
            
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;"><strong>Predicted Flow:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">{flow} m3/h</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;"><strong>Predicted TDS:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">{tds} ppm</td>
                </tr>
                <tr>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0;"><strong>Water Quality:</strong></td>
                    <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; text-align: right;">
                        <span style="background-color: {status_color}; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold;">
                            {quality}
                        </span>
                    </td>
                </tr>
            </table>

            <h2 style="color: #1e293b;">AI Diagnostic Reasoning</h2>
            <div style="background-color: #f1f5f9; padding: 15px; border-left: 4px solid {status_color}; border-radius: 4px; color: #334155; line-height: 1.6;">
                {formatted_report}
            </div>
            
            <p style="margin-top: 30px; font-size: 12px; color: #94a3b8; text-align: center;">
                This is an automated message from your SwarmFlow AI Agent.
            </p>
        </div>
    </div>
    """
    return body