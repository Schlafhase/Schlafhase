#!/usr/bin/env python3

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path


def fetch_wakatime_stats(api_key: str, days: int = 7) -> dict:
    url = "https://hackatime.hackclub.com/api/v1/users/Schlafhase/stats"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()
  

def generate_markdown(stats: dict) -> str:
    data = stats.get("data")
    
    if not data:
        return "No data available.\n"

    total_seconds = data.total_seconds
    total_time_human = data.human_readable_total
    languages = data.languages  
    
    languages = sorted(languages.items(), key=lambda x: x.total_seconds, reverse=True)
    editors = sorted(editors.items(), key=lambda x: x.total_seconds, reverse=True)
    projects = sorted(projects.items(), key=lambda x: x.total_seconds, reverse=True)
    
    md += f"-# Last updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
    md += f"**Total time:** {total_time_human}\n\n"
    md += "**Current editor:** [Neovim](https://neovim.io/)\n\n"
    
    md += "## Languages\n\n"
    for lang in languages[:15]:
        percentage = (lang.total_seconds / total_seconds * 100) if total_seconds > 0 else 0
        md += f"- **{lang.name}**: {format_duration(seconds)} ({percentage:.1f}%)\n"
    
    return md


def main():
    api_key = os.environ.get("WAKATIME_TOKEN")
    if not api_key:
        print(os.environ)
        raise ValueError("WAKATIME_TOKEN environment variable not set")
    
    stats_dir = Path("stats")
    stats_dir.mkdir(exist_ok=True)
    
    print("Fetching Wakatime statistics...")
    stats = fetch_wakatime_stats(api_key)
    
    json_path = stats_dir / "wakatime.json"
    with open(json_path, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Saved raw data to {json_path}")
    
    # Generate and save markdown
    markdown = generate_markdown(stats)
    md_path = stats_dir / "wakatime.md"
    with open(md_path, "w") as f:
        f.write(markdown)
    print(f"Saved markdown to {md_path}")
    
    print("Done!")


if __name__ == "__main__":
    main()
