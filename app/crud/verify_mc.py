def mock_verify_mc(mc_number: str):
    if not mc_number.isdigit() or len(mc_number) != 7:
        return None

    return {
        "mc_number": mc_number,
        "status": "Authorized",
        "company_name": "Example Carrier Inc.",
        "active": True,
    }
