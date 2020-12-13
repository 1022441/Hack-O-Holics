import pandas as pd
from textwrap import wrap

activity_log = pd.read_excel("input/acitivity_log.xlsx")
project_list = activity_log["projectid"].unique().tolist()
fired_hours = pd.read_excel("input/fired_hours.xlsx")


responsible_ebs = activity_log["responsible_ebs"].unique().tolist()

activity_log["responsible_ebs"] = ["<br>".join(wrap(l, 25)) for l in
                                 activity_log["responsible_ebs"]]
activity_log["responsible_system"] = ["<br>".join(wrap(l, 25)) for
                                                  l in
                                                  activity_log[
                                                      "responsible_system"]]
activity_log["responsible_group"] = ["<br>".join(wrap(l, 25)) for l
                                                 in
                                                 activity_log[
                                                     "responsible_group"]]
activity_log["responsible_group"] = ["<br>".join(wrap(l, 25))
                                                     for l in
                                                     activity_log[
                                                         "responsible_group"]]
activity_log["label"] = activity_log["responsible_system"] + \
                      "/" + "<br>" + activity_log[
                          "responsible_group"] + "/" + "<br>" + \
                      activity_log["responsible_component"]

activity_log["label"] = activity_log["label"].apply(str.title)
activity_log["label"] = activity_log["responsible_ebs"] + "<br>" + activity_log[
    "label"]


activity_log_count = activity_log.groupby(["label", 'projectid', 'outage_type'])['analysis_status'].value_counts().to_frame()
activity_log_count.rename(columns={"analysis_status": "status_count"}, inplace=True)
activity_log_count.reset_index(inplace=True)
