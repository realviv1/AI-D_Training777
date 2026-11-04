import { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { initialEvents } from "./data/events";
import { loadRegistrations, saveRegistrations } from "./utils/storage";
import Navbar from "./components/Navbar";
import Events from "./pages/Events";
import Registrations from "./pages/Registrations";
import EmptyState from './components/EmptyState';

export default function App() {
  const [registrations, setRegistrations] = useState(loadRegistrations);

  useEffect(() => {
    saveRegistrations(registrations);
  }, [registrations]);

  function getAvailableSeats(eventId) {
    const event = initialEvents.find((item) => item.id === eventId);
    if (!event) return 0;

    const activeRegistrations = registrations.filter(
      (registration) => registration.eventId === eventId
    ).length;

    return Math.max(0, event.capacity - activeRegistrations);
  }

  function registerUser(eventId, name, email) {
    const cleanName = name.trim();
    const cleanEmail = email.trim().toLowerCase();

    if (!cleanName) {
      return { success: false, message: "Please enter your full name." };
    }

    if (!cleanEmail) {
      return { success: false, message: "Please enter your email address." };
    }

    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(cleanEmail)) {
      return { success: false, message: "Please enter a valid email address." };
    }

    const event = initialEvents.find((item) => item.id === eventId);
    if (!event) {
      return { success: false, message: "The selected event could not be found." };
    }

    if (getAvailableSeats(eventId) <= 0) {
      return { success: false, message: "Sorry, this event is fully booked." };
    }

    const alreadyRegistered = registrations.some(
      (registration) =>
        registration.eventId === eventId &&
        registration.email.trim().toLowerCase() === cleanEmail
    );

    if (alreadyRegistered) {
      return {
        success: false,
        message: "This email address is already registered for this event."
      };
    }

    const newRegistration = {
      id: globalThis.crypto?.randomUUID
        ? globalThis.crypto.randomUUID()
        : `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      eventId,
      name: cleanName,
      email: cleanEmail,
      status: "active",
      registeredAt: new Date().toISOString()
    };

    setRegistrations((current) => [...current, newRegistration]);
    return { success: true, message: "Registration successful. Your seat is reserved!" };
  }

  function cancelRegistration(registrationId) {
    const confirmed = window.confirm(
      "Are you sure you want to cancel this registration?"
    );

    if (!confirmed) return;

    setRegistrations((current) =>
      current.filter((registration) => registration.id !== registrationId)
    );
  }

  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar registrationCount={registrations.length} />
        <Routes>
          <Route
            path="/"
            element={
              <Events
                events={initialEvents}
                getAvailableSeats={getAvailableSeats}
                registerUser={registerUser}
              />
            }
          />
          <Route
            path="/registrations"
            element={
              <Registrations
                events={initialEvents}
                registrations={registrations}
                cancelRegistration={cancelRegistration}
              />
            }
          />
          <Route
            path="*"
            element={
              <main className="page-container">
                <EmptyState
                  title="Page not found"
                  message="The page you're looking for does not exist."
                />
              </main>
            }
          />
        </Routes>
        <footer className="site-footer">
          <span>GATHER<span className="brand-dot">.</span></span>
          <span>Make room for something new.</span>
        </footer>
      </div>
    </BrowserRouter>
  );
}