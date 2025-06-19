import asyncio
import json
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.cloud import pubsub_v1
from repositories.insight_repository import InsightRepository
from services.insight_service import InsightService
from core.pubsub_client import PubSubClient
from core.websocket_manager import websocket_manager
from config import settings
from database import AsyncSessionLocal, create_db_and_tables
from models.clinical_insight import ClinicalInsightCreate

# --- Initialization for the agent ---
pubsub_client = PubSubClient()
bigquery_client = bigquery.Client(project=settings.GCP_PROJECT_ID)

async def get_insight_service_for_agent():
    """Helper to get InsightService with a new DB session for the agent."""
    async for db_session in AsyncSessionLocal():
        insight_repo = InsightRepository(db_session)
        yield InsightService(insight_repo, pubsub_client)

# --- BigQuery Query Function ---
async def query_user_activity_trends(time_period_hours: int = 24) -> dict:
    """
    Queries BigQuery for user activity trends over a specified time period.
    This is a simplified example; real trend analysis would be more complex.
    Returns:
        dict: A dictionary summarizing trends, e.g., activity counts per user.
    """
    table_id = f"{settings.GCP_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.{settings.BIGQUERY_TABLE_USER_ACTIVITY}"

    # Calculate the timestamp N hours ago
    start_time = datetime.utcnow() - timedelta(hours=time_period_hours)

    query = f"""
    SELECT
        user_id,
        activity_type,
        COUNT(*) as activity_count
    FROM
        `{table_id}`
    WHERE
        timestamp >= '{start_time.isoformat()}'
    GROUP BY
        user_id, activity_type
    ORDER BY
        user_id, activity_count DESC
    """

    print(f"Trend Monitoring Agent: Running BigQuery query for last {time_period_hours} hours...")

    job_config = bigquery.QueryJobConfig()
    query_job = bigquery_client.query(query, job_config=job_config)

    results = {}
    try:
        rows = list(query_job.result()) # Wait for the job to complete
        for row in rows:
            user_id = row["user_id"]
            if user_id not in results:
                results[user_id] = []
            results[user_id].append({
                "activity_type": row["activity_type"],
                "count": row["activity_count"]
            })
        print(f"Trend Monitoring Agent: BigQuery query complete. Found data for {len(results)} users.")
    except Exception as e:
        print(f"Trend Monitoring Agent: BigQuery query failed: {e}")
    return results

# --- Main Trend Monitoring Logic ---
async def monitor_trends():
    """
    Monitors trends in user activity data from BigQuery and generates insights.
    This function will be called periodically.
    """
    print("Trend Monitoring Agent: Starting trend analysis cycle...")
    trends_data = await query_user_activity_trends(time_period_hours=24) # Analyze last 24 hours

    if not trends_data:
        print("Trend Monitoring Agent: No significant trends found or no data in BigQuery.")
        return

    for user_id, activities in trends_data.items():
        trend_summary = f"User {user_id} activity trends in last 24h: "
        for activity in activities:
            trend_summary += f"{activity['activity_type']} ({activity['count']}), "
        trend_summary = trend_summary.rstrip(', ') + "."

        print(f"Trend Monitoring Agent: Analyzing trends for user {user_id}: {trend_summary}")

        # Simulate AI analysis for trend insight
        async for insight_service in get_insight_service_for_agent():
            insight_text_from_ai = await insight_service.generate_insight_with_ai(
                user_id,
                trend_summary,
                "trend_analysis",
                None # No specific source ID for aggregated trend
            )

            insight_create_data = ClinicalInsightCreate(
                user_id=user_id,
                source_type="trend_analysis",
                source_id=None,
                insight_text=insight_text_from_ai,
                severity="low", # Placeholder
                recommendations="Review user's recent activity for patterns."
            )
            new_insight = await insight_service.create_clinical_insight(insight_create_data)

            if new_insight:
                print(f"Trend Monitoring Agent: Generated and stored trend insight for user {user_id}: {new_insight.id}")
                await websocket_manager.send_to_user(
                    user_id,
                    "new_clinical_insight",
                    {"insight": new_insight.model_dump()}
                )
            else:
                print(f"Trend Monitoring Agent: Failed to create trend insight.")

async def main_trend_monitoring_agent(interval_seconds: int = 3600): # Run once every hour (3600 seconds)
    """Main function to run the Trend Monitoring Agent periodically."""
    print(f"Starting Trend Monitoring Agent, running every {interval_seconds} seconds...")
    await create_db_and_tables()

    while True:
        try:
            await monitor_trends()
        except Exception as e:
            print(f"Trend Monitoring Agent: Error during monitoring cycle: {e}")
        await asyncio.sleep(interval_seconds) # Wait before next cycle

if __name__ == "__main__":
    # To run this agent standalone for testing:
    # python -m agents.trend_monitoring_agent
    asyncio.run(main_trend_monitoring_agent())