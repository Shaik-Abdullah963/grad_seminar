class ProfilingModule:
    """
    ProfilingModule handles user profile management.
    """
    def __init__(self):
        # Initialize the user profile with default values.
        self.profile = {
            "name": None,
            "preferences": [],
            "interaction_count": 0
        }
    
    def get_profile(self):
        """Return the current user profile."""
        return self.profile

    def update_profile(self, key, value):
        """Update the profile with a given key-value pair."""
        self.profile[key] = value

    def add_preference(self, preference):
        """Add a new preference to the profile if not already present."""
        if preference not in self.profile.get("preferences", []):
            self.profile.setdefault("preferences", []).append(preference)

    def increment_interaction_count(self):
        """Increment the count of user interactions."""
        self.profile["interaction_count"] += 1

    def clear_profile(self):
        """Reset the user profile to default values."""
        self.profile = {
            "name": None,
            "preferences": [],
            "interaction_count": 0
        }