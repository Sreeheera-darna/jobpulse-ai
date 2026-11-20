import json
import subprocess
files = [
    "backend/india_jobs.json",
    "backend/india_jobs_classified.json"
]
for f in files:
    print("\nFILE:", f)
    for stage, label in [(2, "GITHUB"), (3, "LOCAL")]:
        result = subprocess.run(
            ["git", "show", f":{stage}:{f}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            classified = sum(
                isinstance(j.get("ai_classification"), dict)
                for j in data
            )
            print(f"{label}: Jobs={len(data)}, Classified={classified}")
        else:
            print(f"{label}: ERROR - {result.stderr.strip()}")
