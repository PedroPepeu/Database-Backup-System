#!/usr/bin/env python3
# monitor.py - Generate dashboard data for backup monitoring

import json
import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

BACKUP_DIR = "/opt/backups"
REPORT_DIR = "/opt/backups/reports"
HISTORY_FILE = os.path.join(BACKUP_DIR, "backup_history.json")

def ensure_dir(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)

def parse_backup_history():
    """Parse the backup history JSON file into a pandas DataFrame"""
    if not os.path.exists(HISTORY_FILE):
        return pd.DataFrame()
    
    # Read backup history line by line (each line is a separate JSON object)
    backups = []
    with open(HISTORY_FILE, 'r') as f:
        for line in f:
            try:
                backup = json.loads(line.strip())
                backups.append(backup)
            except json.JSONDecodeError:
                continue
    
    if not backups:
        return pd.DataFrame()
    
    # Convert to DataFrame
    df = pd.DataFrame(backups)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def generate_backup_size_chart(df):
    """Generate a chart showing backup sizes over time"""
    if df.empty:
        return
    
    # Extract size in MB for visualization
    df['size_mb'] = df['size'].str.replace('M', '').astype(float)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['timestamp'], df['size_mb'], marker='o')
    plt.title('Database Backup Sizes Over Time')
    plt.xlabel('Date')
    plt.ylabel('Size (MB)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    ensure_dir(REPORT_DIR)
    plt.savefig(os.path.join(REPORT_DIR, 'backup_sizes.png'))

def generate_dashboard_html():
    """Generate an HTML dashboard with backup statistics"""
    df = parse_backup_history()
    if df.empty:
        html_content = "<html><body><h1>No backup history available</h1></body></html>"
    else:
        # Generate backup size chart
        generate_backup_size_chart(df)
        
        # Calculate statistics
        latest_backup = df.iloc[-1]
        total_backups = len(df)
        avg_size = df['size'].iloc[-5:].to_list() if len(df) >= 5 else df['size'].to_list()
        
        # Create HTML report
        html_content = f"""
        <html>
        <head>
            <title>Database Backup Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .dashboard {{ max-width: 1000px; margin: 0 auto; }}
                .stats {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
                .stat-card {{ background: #f5f5f5; border-radius: 8px; padding: 15px; flex: 1; min-width: 200px; }}
                .chart {{ margin-top: 30px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="dashboard">
                <h1>Database Backup Dashboard</h1>
                <div class="stats">
                    <div class="stat-card">
                        <h3>Latest Backup</h3>
                        <p>Date: {latest_backup['timestamp'].strftime('%Y-%m-%d %H:%M')}</p>
                        <p>Size: {latest_backup['size']}</p>
                        <p>Status: {latest_backup['status']}</p>
                    </div>
                    <div class="stat-card">
                        <h3>Backup History</h3>
                        <p>Total Backups: {total_backups}</p>
                        <p>Recent Sizes: {', '.join(avg_size)}</p>
                    </div>
                </div>
                
                <div class="chart">
                    <h2>Backup Size Trend</h2>
                    <img src="reports/backup_sizes.png" alt="Backup Size Trend" style="max-width: 100%;">
                </div>
                
                <h2>Recent Backups</h2>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>File</th>
                        <th>Size</th>
                        <th>Status</th>
                    </tr>
        """
        
        # Add the most recent 10 backups to the table
        for _, row in df.iloc[-10:].iterrows():
            html_content += f"""
                    <tr>
                        <td>{row['timestamp'].strftime('%Y-%m-%d %H:%M')}</td>
                        <td>{row['file']}</td>
                        <td>{row['size']}</td>
                        <td>{row['status']}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
    
    # Write HTML to file
    ensure_dir(REPORT_DIR)
    with open(os.path.join(REPORT_DIR, 'dashboard.html'), 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_dashboard_html()
    print("Dashboard generated successfully!")