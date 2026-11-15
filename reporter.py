def display_report(scan_result, risk_result):

    print("\n")
    print("=" * 55)
    print("                 METAPEEK")
    print("             METADATA SCANNER")
    print("=" * 55)

    if "error" in scan_result:
        print("\n[ERROR]", scan_result["error"])
        return

    print("\n[FILE INFORMATION]")

    for key, value in scan_result.items():
        if key not in (
            "metadata",
            "gps_found",
            "gps_coordinates",
            "maps_url"
        ):
            print(f"{key}: {value}")

    print("\n[EXTRACTED METADATA]")

    metadata = scan_result.get("metadata", {})

    if metadata:
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print("No readable metadata found.")

    print("\n[GPS INFORMATION]")

    if scan_result.get("gps_found"):
        print("GPS metadata detected.")

        coordinates = scan_result.get("gps_coordinates")

        if coordinates:
            latitude = coordinates["latitude"]
            longitude = coordinates["longitude"]

            print(f"Latitude: {latitude}")
            print(f"Longitude: {longitude}")
            print(
                "Google Maps:",
                scan_result["maps_url"]
            )
        else:
            print("GPS detected, but valid coordinates unavailable.")
    else:
        print("No GPS metadata found.")

    print("\n[PRIVACY RISK ANALYSIS]")
    print("Overall Risk:", risk_result["risk_level"])

    risks = risk_result.get("risks", [])

    if risks:
        for risk in risks:
            print("\nFinding:", risk["finding"])
            print("Severity:", risk["severity"])
            print("Details:", risk["description"])
    else:
        print("No known risks detected.")

    print("\n" + "=" * 55)
    print("         SCAN COMPLETED")
    print("=" * 55 + "\n")
