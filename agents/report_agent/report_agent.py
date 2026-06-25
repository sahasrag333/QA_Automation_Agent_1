from pathlib import Path
from datetime import datetime


class ReportAgent:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.report_dir = self.project_root / "framework" / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        test_name,
        status,
        execution_time,
        error_type="N/A",
        root_cause="N/A",
        suggested_fix="N/A",
    ):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        html_content = f"""
<html>
<head>
    <title>AI QA Automation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 30px;
        }}
        .pass {{
            color: green;
            font-size: 24px;
        }}
        .fail {{
            color: red;
            font-size: 24px;
        }}
        .section {{
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1>AI QA Automation Report</h1>

    <div class="section">
        <h2>Execution Summary</h2>
        <p><b>Test Name:</b> {test_name}</p>
        <p><b>Status:</b> <span class="{status.lower()}">{status}</span></p>
        <p><b>Execution Time:</b> {execution_time}</p>
        <p><b>Execution Date:</b> {timestamp}</p>
    </div>

    <div class="section">
        <h2>Failure Analysis</h2>
        <p><b>Error Type:</b> {error_type}</p>
        <p><b>Root Cause:</b> {root_cause}</p>
        <p><b>Suggested Fix:</b> {suggested_fix}</p>
    </div>
</body>
</html>
"""

        latest_report = self.report_dir / "latest_report.html"
        history_report = self.report_dir / f"run_{timestamp}.html"

        latest_report.write_text(html_content, encoding="utf-8")
        history_report.write_text(html_content, encoding="utf-8")

        print(f"\nReport Generated:\n{latest_report}")


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    report_agent = ReportAgent(project_root)
    report_agent.generate_report(
        test_name="button_click",
        status="PASS",
        execution_time="3.25 sec",
    )


