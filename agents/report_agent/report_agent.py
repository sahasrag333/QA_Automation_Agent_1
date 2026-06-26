from pathlib import Path
from datetime import datetime


class ReportAgent:

    def __init__(self, project_root):

        self.project_root = Path(project_root)

        self.report_dir = (
            self.project_root
            / "framework"
            / "reports"
        )

        self.report_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def generate_report(

        self,

        test_name,

        status,

        execution_time,

        error_type="N/A",

        root_cause="N/A",

        suggested_fix="N/A",

        healing_history=None

    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        # ------------------------------------
        # Healing Summary
        # ------------------------------------

        healing_html = ""

        if healing_history:

            healing_html = """
            <div class="section">

                <h2>Healing Attempts</h2>
            """

            for item in healing_history:

                healing_html += f"""

                <div class="heal">

                    <p>

                    <b>Attempt :</b> {item['attempt']}<br>

                    <b>Status :</b> {item['status']}<br>

                    <b>Error :</b> {item['error_type']}

                    </p>

                </div>

                """

            healing_html += "</div>"

        # ------------------------------------
        # HTML
        # ------------------------------------

        html_content = f"""

<html>

<head>

<title>AI QA Automation Report</title>

<style>

body {{

font-family: Arial;

margin:40px;

background:#f7f7f7;

}}

.section {{

background:white;

padding:20px;

margin-bottom:20px;

border-radius:8px;

box-shadow:0px 0px 6px #ccc;

}}

.pass {{

color:green;

font-weight:bold;

font-size:20px;

}}

.fail {{

color:red;

font-weight:bold;

font-size:20px;

}}

.heal {{

padding:10px;

margin-top:10px;

border-left:4px solid #2196F3;

background:#eef6ff;

}}

</style>

</head>

<body>

<h1>AI QA Automation Report</h1>

<div class="section">

<h2>Execution Summary</h2>

<p><b>Test Name :</b> {test_name}</p>

<p><b>Status :</b>

<span class="{status.lower()}">

{status}

</span>

</p>

<p>

<b>Execution Time :</b>

{execution_time}

</p>

<p>

<b>Execution Date :</b>

{timestamp}

</p>

</div>

<div class="section">

<h2>Failure Analysis</h2>

<p>

<b>Error Type :</b>

{error_type}

</p>

<p>

<b>Root Cause :</b>

{root_cause}

</p>

<p>

<b>Suggested Fix :</b>

{suggested_fix}

</p>

</div>

{healing_html}

</body>

</html>

"""

        latest_report = (
            self.report_dir
            / "latest_report.html"
        )

        history_report = (
            self.report_dir
            / f"run_{timestamp}.html"
        )

        latest_report.write_text(

            html_content,

            encoding="utf-8"

        )

        history_report.write_text(

            html_content,

            encoding="utf-8"

        )

        print(

            f"\nReport Generated:\n{latest_report}"

        )


if __name__ == "__main__":

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    report = ReportAgent(
        project_root
    )

    report.generate_report(

        test_name="widget_click",

        status="FAIL",

        execution_time="12 sec",

        error_type="TimeoutException",

        root_cause="Locator not found",

        suggested_fix="Use contains(text())",

        healing_history=[

            {

                "attempt": 1,

                "status": "PASS",

                "error_type": "TimeoutException"

            },

            {

                "attempt": 2,

                "status": "FAIL",

                "error_type": "ElementNotInteractable"

            }

        ]

    )