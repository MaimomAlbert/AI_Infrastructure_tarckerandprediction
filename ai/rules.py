def assign_status(progress_percent):
    """
    Simple rule-based status assignment
    """
    if progress_percent is None:
        return "Unknown"
    if progress_percent < 40:
        return "Delayed"
    elif progress_percent < 70:
        return "At Risk"
    else:
        return "On Track"
