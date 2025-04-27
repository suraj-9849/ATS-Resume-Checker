
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt
def create_activity_chart(github_info):
    """Create chart of repository activity over time"""
    if "error" in github_info or not github_info.get("repos"):
        return None

    dates = [
        datetime.strptime(repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
        for repo in github_info["repos"]
    ]

    # Count repos by month
    df = pd.DataFrame({"date": dates})
    df["month"] = df["date"].dt.strftime("%Y-%m")
    monthly_counts = df.groupby("month").size().reset_index(name="count")
    monthly_counts = monthly_counts.sort_values("month")

    # Ensure we have at least 12 months of data
    if len(monthly_counts) < 12:
        all_months = (
            pd.date_range(
                start=min(dates).replace(day=1),
                end=max(dates).replace(day=1),
                freq="MS",
            )
            .strftime("%Y-%m")
            .tolist()
        )

        # Fill in missing months with zero counts
        month_dict = {m: 0 for m in all_months}
        for _, row in monthly_counts.iterrows():
            month_dict[row["month"]] = row["count"]

        monthly_counts = pd.DataFrame(
            {"month": list(month_dict.keys()), "count": list(month_dict.values())}
        )

    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(monthly_counts["month"], monthly_counts["count"])
    plt.xticks(rotation=45)
    plt.title("Repository Activity by Month")
    plt.xlabel("Month")
    plt.ylabel("Number of Updates")
    plt.tight_layout()

    return fig
