# A global dictionary to hold the Event objects for each session
# { "session_id": threading.Event() }
approval_events = {}

# { "session_id": True/False }
approval_results = {}
