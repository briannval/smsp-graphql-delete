import requests

from config import perdoo_headers, perdoo_id, perdoo_url, perdoo_user_id

perdoo_id_keys = list(perdoo_id.keys())

print("Please choose")
for i, v in enumerate(perdoo_id_keys):
    print(f"{i+1}. {v}")
choice = int(input("> "))

print("Input cutoff date in YYYY-MM-DD format")
date_variable = input("> ")

selected_kpi = perdoo_id_keys[choice - 1]

selected_kpi_id = perdoo_id[selected_kpi]

to_be_deleted_commits = []

try:
    resp = requests.post(
        perdoo_url,
        json={
            "query": f"""
              query all_commit {{
                allCommits(
                  user_Id: "{perdoo_user_id}"
                  commitDate_Lte: "{date_variable}T16:59:59+00:00"
                ) {{
                  edges {{
                    node {{
                      id
                      commitDate
                      value
                      kpi {{
                        id
                        name
                      }}
                    }}
                  }}
                }}
              }}
              """
        },
        headers=perdoo_headers,
    )
    res = resp.json()
    all_commits = res["data"]["allCommits"]["edges"]

    for commit in all_commits:
        commit_id = commit["node"]["id"]
        commit_kpi_id = commit["node"]["kpi"]["id"]
        if commit_kpi_id == selected_kpi_id:
            to_be_deleted_commits.append(commit_id)

    for to_be_deleted_commit in to_be_deleted_commits:
        try:
            requests.post(
                perdoo_url,
                json={
                    "query": f"""
                      mutation delete_commit {{
                        deleteCommit(input: {{id: "{to_be_deleted_commit}"}}) {{
                          commit {{
                            id
                            kpi {{
                              name
                            }}
                            value
                          }}
                          errors {{
                            field
                            messages
                          }}
                        }}
                      }}
                      """
                },
                headers=perdoo_headers,
            )
            print(
                f"Succeeded deleting commit {to_be_deleted_commit} for {selected_kpi}",
            )
        except Exception as err:
            print(
                f"Failed deleting commit {to_be_deleted_commit} for {selected_kpi}",
                err,
            )

except Exception as err:
    print(
        "ERROR",
        err,
    )
