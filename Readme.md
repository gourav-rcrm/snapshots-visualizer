## rm -rf Snapshots Web UI

This repository contains a simple web application to list EC2 snapshots and perform deletion operations on them using a user-friendly web interface.

### Instructions to Run

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/ec2-snapshots-web-ui.git
cd ec2-snapshots-web-ui
```

2. Install the required dependencies:

Make sure you have Python and pip installed on your machine. Then, run the following command:

```bash
pip install boto3 Flask pytz
```

3. Set up AWS CLI Credentials:

Before running the application, make sure you have configured AWS CLI with your IAM user credentials. Ensure that the user has the necessary permissions to interact with EC2 and its snapshots.

4. Run the Web Application:

```bash
python app.py
```

The application will start running on your local machine, and you can access it through your web browser by visiting `http://localhost:5000/`.

5. View EC2 Snapshots:

The web interface will display a table containing all your EC2 snapshots, sorted by date of creation in ascending order. Snapshots are segregated based on their creation date for easy navigation.

6. Delete Snapshots:

You can delete a snapshot by clicking the "Delete" button next to the corresponding snapshot. Be cautious while deleting, as it's irreversible.

### Additional Notes

- This web application uses the Flask micro-framework for Python to provide the web interface.
- The UI is styled using Tailwind CSS CDN for a clean and modern look.
- Ensure that you have an active internet connection to access the Tailwind CSS CDN.
- For security reasons, make sure to use appropriate authentication and authorization mechanisms before deploying this application to production.

**Enjoy managing your EC2 snapshots with ease using this web interface!**