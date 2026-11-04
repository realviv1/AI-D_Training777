const STORAGE_KEY = "event_enrollment_registrations";

export function loadRegistrations() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (!saved) return[];
        const parsed = JSON.parse(saved);
        return Array.isArray(parsed) ? parsed : [];
    }   catch (error) {
        console.error("Couls not read saved registrations:", error);
        return [];
    }
}

export function saveRegistrations(registrations) {
    try {
        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(registrations)
        );
    } catch (error) {
        console.error("Couls not save registrations:", error);
    }
}

export { STORAGE_KEY };