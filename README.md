# MRMS Medical Resource Management System

MRMS is a web application designed to streamline medical resource management for patients, doctors, hospitals, and administrators. With MRMS, users can search for hospitals, check doctors working in those hospitals, book appointments, view hospital facilities, and book lab tests.

## Features

- **Hospital Search**: Users can search for hospitals based on location, specialty, or services offered.
- **Doctor Information**: Users can view information about doctors working in selected hospitals, including their specialties, availability, and contact details.
- **Appointment Booking**: Patients can book appointments with doctors at their preferred time slots.
- **Facility Check**: Users can check the facilities available at hospitals, such as diagnostic services, operation theaters, and ICU facilities.
- **Lab Test Booking**: Patients can book laboratory tests at affiliated labs or hospitals.

## Technologies Used

- **Python Django**: Backend web framework for building the MRMS application.
- **Bootstrap**: Frontend framework for responsive and mobile-friendly design.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/mrms.git
   ```

2. Navigate to the project directory:

   ```bash
   cd mrms
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the development server:

   ```bash
   python manage.py runserver
   ```

6. Access the application at [http://localhost:8000](http://localhost:8000) in your web browser.

## Usage

- **User Registration**: Sign up for a new account or log in if you already have one.
- **Hospital Search**: Search for hospitals based on location, specialty, or services.
- **Doctor Information**: View details of doctors working in selected hospitals.
- **Appointment Booking**: Book appointments with preferred doctors at available time slots.
- **Facility Check**: Check hospital facilities available for patients.
- **Lab Test Booking**: Book laboratory tests at affiliated labs or hospitals.

## Contributing

Contributions to MRMS are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.