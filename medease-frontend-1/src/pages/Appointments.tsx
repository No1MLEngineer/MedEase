import React from 'react';
import AppointmentScheduler from '../components/Appointments/AppointmentScheduler';

const Appointments: React.FC = () => {
    return (
        <div>
            <h1>Schedule an Appointment</h1>
            <AppointmentScheduler />
        </div>
    );
};

export default Appointments;