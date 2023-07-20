import boto3
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone
import pytz

app = Flask(__name__)

def get_snapshot_date(snapshot):
    return snapshot.start_time

def list_snapshots():
    # Create an AWS session using your CLI credentials
    session = boto3.Session(profile_name='default')
    # Create an EC2 resource object
    ec2_resource = session.resource('ec2')
    # Retrieve all the snapshots owned by you
    snapshots = list(ec2_resource.snapshots.filter(OwnerIds=['self']))
    # Sort snapshots by date of creation in ascending order
    sorted_snapshots = sorted(snapshots, key=get_snapshot_date)
    # Get the current date and time
    current_datetime = datetime.now(timezone.utc)
    # Create dictionaries to store snapshots based on date
    snapshots_by_date = {}
    # Define the GMT+5:30 timezone
    gmt_timezone = pytz.timezone('Asia/Kolkata')
    # Iterate through the sorted snapshots and segregate them based on date
    for snapshot in sorted_snapshots:
        snapshot_date = get_snapshot_date(snapshot)
        # Skip snapshots that are created after the current date and time
        if snapshot_date > current_datetime:
            continue
        # Convert the snapshot's start time to the GMT+5:30 timezone
        snapshot_date_gmt = snapshot_date.astimezone(gmt_timezone)
        # Calculate the age of the snapshot
        age = current_datetime - snapshot_date
        # Extract the date and time as strings
        date_str = snapshot_date_gmt.strftime('%Y-%m-%d')
        time_str = snapshot_date_gmt.strftime('%H:%M:%S')
        
        # Create a new list for the date if it doesn't exist
        if date_str not in snapshots_by_date:
            snapshots_by_date[date_str] = []
        
        # Append the snapshot to the list for the corresponding date
        snapshots_by_date[date_str].append({
            'SnapshotId': snapshot.id,
            'CreationTime (GMT+5:30)': time_str,
            'Age (in days)': age.days
        })
    
    # Print the snapshots by date in ascending order
    for date, snapshots in sorted(snapshots_by_date.items()):
        print(f'Snapshots created on {date}:')
        for snapshot in snapshots:
            print(f"  - Snapshot ID: {snapshot['SnapshotId']}")
            print(f"    Creation Time (GMT+5:30): {snapshot['CreationTime (GMT+5:30)']}")
            print(f"    Age (in days): {snapshot['Age (in days)']}")
        print()
    return snapshots_by_date
@app.route('/')
def index():
    snapshots_data = list_snapshots()
    return render_template('index.html', snapshots_data=snapshots_data)

@app.route('/delete_snapshot', methods=['POST'])
def delete_snapshot():
    snapshot_id = request.json.get('snapshot_id')
    if not snapshot_id:
        return jsonify({'success': False, 'message': 'Snapshot ID is missing'})

    # Create an AWS session using your CLI credentials
    session = boto3.Session(profile_name='default')
    # Create an EC2 resource object
    ec2_resource = session.resource('ec2')
    # Delete the snapshot
    try:
        snapshot = ec2_resource.Snapshot(snapshot_id)
        snapshot.delete()
        return jsonify({'success': True, 'message': 'Snapshot deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)