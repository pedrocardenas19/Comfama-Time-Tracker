import matplotlib.pyplot as plt
import io
import base64

def generate_pie_chart(project):
    completed_hours = sum(report.time_spent for category in project.task_categories.all() for report in category.task_reports.all())
    remaining_hours = project.required_hours - completed_hours
    remaining_hours = max(remaining_hours, 0)  # Ensure it doesn't go negative

    fig, ax = plt.subplots()
    ax.pie([completed_hours, remaining_hours], labels=['Completed', 'Remaining'], autopct='%1.1f%%', colors=['#4caf50', '#ff9800'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64
