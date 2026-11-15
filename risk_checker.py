def check_risks(scan_result):
    """
    Identify potentially sensitive information
    in extracted file metadata.
    """

    risks = []

    if "error" in scan_result:
        return {
            "risk_level": "UNKNOWN",
            "risks": ["File could not be scanned."]
        }

    metadata = scan_result.get("metadata", {})

    # Check GPS information
    if scan_result.get("gps_found"):
        risks.append({
            "finding": "GPS information detected",
            "severity": "HIGH",
            "description": "The image may contain location information."
        })

    # Check author information
    for key in metadata:
        key_lower = key.lower()

        if key_lower in ["artist", "author", "owner"]:
            risks.append({
                "finding": f"Author information detected: {key}",
                "severity": "MEDIUM",
                "description": "The file may reveal information about its creator."
            })

        # Check timestamps
        if "date" in key_lower or "time" in key_lower:
            risks.append({
                "finding": f"Timestamp detected: {key}",
                "severity": "LOW",
                "description": "The file may reveal when it was created or captured."
            })

    # Determine overall risk
    if any(r["severity"] == "HIGH" for r in risks):
        risk_level = "HIGH"
    elif any(r["severity"] == "MEDIUM" for r in risks):
        risk_level = "MEDIUM"
    elif risks:
        risk_level = "LOW"
    else:
        risk_level = "NO KNOWN RISKS DETECTED"

    return {
        "risk_level": risk_level,
        "risks": risks
    }
