DICT_GROUP = {
    1: 'admin',
    2: 'deparment_supervisior',
    3: 'incident_manager'
}

status_true = {
    "status": True
}

status_false = {
    "status": False
}

DICT_REPORT_STATUS = {
    0: 'Generating Report',
    1: 'Generated',
    2: 'No Data Found'
}


DICT_INCIDENT_DATA = {
    "priority": {
        1: "High",
        2: "High",
        3: "Medium",
        4: "Low",
        5: "Low"
    },
    "category": {
        1: "People Safety",
        2: "Plant Productivity"
    },
    "location": {
        1: "Machine",
        2: "Washine Area"
    },
    "status": {
        1: "Resolved",
        2: "Unresolved",
        3: "New",
        4: "Reject"
    },
}

DICT_CAMERA_LIST = {
    "Cam3": {
        "camera_name": "Wash Feeding",
        "camera_id": 3,
        "analysis_table": F'''argus."1005_camera3_analysis" '''
    },
    "Cam2":  {
        "camera_name": "Sorting Belt 2",
        "camera_id": 2,
        "analysis_table": F'''argus."1005_camera2_analysis" ''',
        "analysis_counter_table": F'''argus."1005_camera2_analysis_counter" ''',
        "belt_analysis_table": F'''argus."1005_camera2_belt_analysis" ''',
    },
    "Cam8": {
        "camera_name": "Unit 1 Gate",
        "camera_id": 8,
        "analysis_table": F'''argus."1005_camera8_analysis" ''',
    },
    "Cam9": {
        "camera_name": "Sorting Belt 1",
        "camera_id": 9,
        "analysis_table": F'''argus."1005_camera9_analysis" ''',
        "analysis_counter_table": F'''argus."1005_camera9_analysis_counter" ''',
        "belt_analysis_table": F'''argus."1005_camera9_belt_analysis" ''',
    },

}
