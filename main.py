import boto3
import paramiko
import time


def main():
    ec2 = boto3.resource('ec2')
    instance_id = 'i-xxxxxxx'  # Replace with your actual instance ID
    user = 'ubuntu'  # Default user for Ubuntu AMI
    key_path = 'ssh_keyfile.pem'  # Path to your private SSH key

    # Ask for the hash
    hash_input = input("Enter the hash: ")

    # Connect to the instance
    instance = ec2.Instance(instance_id)
    instance.start()
    instance.wait_until_running()

    # Update instance information
    instance.load()

    # SSH into the instance
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=instance.public_dns_name, username=user, key_filename=key_path)

    # Place the hash as a .txt file
    stdin, stdout, stderr = ssh.exec_command(f'echo "{hash_input}" > /hashes/hash.txt')
    stdout.channel.recv_exit_status()  # Wait for command to complete

    # Start the script
    stdin, stdout, stderr = ssh.exec_command('bash /scripts/crack.sh')
    stdout.channel.recv_exit_status()
    # Check for completion or timeout after 5 minutes
    timeout = 300  # 5 minutes in seconds
    start_time = time.time()
    lock_file_path = '/tmp/crack.lock'

    while time.time() - start_time < timeout:
        stdin, stdout, stderr = ssh.exec_command(f'test -f {lock_file_path}')
        if stdout.channel.recv_exit_status() != 0:
            break  # Lock file does not exist, hence `crack.sh` has finished
        time.sleep(10)  # Check every 10 seconds

    # Retrieve files from /potfile
    sftp = ssh.open_sftp()
    sftp.chdir('/potfile')
    for filename in sftp.listdir():
        sftp.get(f'/potfile/{filename}', f'./{filename}')  # Download to local machine

    # Empty out /potfile and /hashes directories
    ssh.exec_command('rm -rf /potfile/* /hashes/*')

    # Shutdown the instance
    ssh.close()
    instance.stop()


if __name__ == "__main__":
    main()
