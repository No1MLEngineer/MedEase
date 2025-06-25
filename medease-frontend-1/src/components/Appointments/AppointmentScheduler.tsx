import React, { useState } from 'react';
import { DateTime } from 'luxon';
import './AppointmentScheduler.css';

const AppointmentScheduler = () => {
    const [date, setDate] = useState(DateTime.local().toISODate());
    const [time, setTime] = useState('');
    const [patientName, setPatientName] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!patientName || !time) {
            setError('Please fill in all fields.');
            return;
        }
        setError('');
        // Logic to schedule the appointment goes here
        console.log(`Appointment scheduled for ${patientName} on ${date} at ${time}`);
    };

    return (
        <div className="appointment-scheduler">
            <h2>Schedule an Appointment</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="patientName">Patient Name:</label>
                    <input
                        type="text"
                        id="patientName"
                        value={patientName}
                        onChange={(e) => setPatientName(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="date">Date:</label>
                    <input
                        type="date"
                        id="date"
                        value={date}
                        onChange={(e) => setDate(e.target.value)}
                    />
                </div>
                <div>
                    <label htmlFor="time">Time:</label>
                    <input
                        type="time"
                        id="time"
                        value={time}
                        onChange={(e) => setTime(e.target.value)}
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Schedule Appointment</button>
            </form>
        </div>
    );
};

export default AppointmentScheduler;