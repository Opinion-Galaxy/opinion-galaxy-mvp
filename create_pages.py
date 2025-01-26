from src.api import driver
from src.database import get_db_connection

conn = get_db_connection()
topic_driver = driver.Topic(conn)

topics = [row["topic"] for row in topic_driver.get_all()]

# -------------------
# Page
# -------------------
for selected_topic in topics:
    page = f"""
from src.components import footer
from src.template import generate_page

generate_page(selected_topic="{selected_topic}")
footer()
    """
    with open(f"pages/{selected_topic}.py", "w") as f:
        f.write(page)