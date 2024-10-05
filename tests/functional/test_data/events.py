click_event = {
    "event": {
        "event_type": "click",
        "timestamp": "2024-10-03T14:30:00Z",
        "user_id": "956939f6-7a98-4bf1-9949-500e5dd20fa0",
        "country": "US",
        "device": "mobile",
        "element": "button_submit",
        "page_url": "https://example.com/submit",
    }
}

wrong_event_type = {
    "event": {
        "event_type": "some_event",
        "timestamp": "2024-10-03T14:30:00Z",
        "user_id": "956939f6-7a98-4bf1-9949-500e5dd20fa0",
        "country": "US",
        "device": "mobile",
        "element": "button_submit",
        "page_url": "https://example.com/submit",
    }
}

missing_fields = {
    "event": {"event_type": "click", "page_url": "https://example.com/submit"}
}
