class HealthcheckManager:
    """
    Manages the system health status for the API.

    This class is used to check whether the application is running and responsive.
    """

    def status(self) -> dict:
        """
        Returns the current health status of the system.

        Returns:
            dict: A dictionary indicating the system is operational.
        """
        return {"status": "ok"}
