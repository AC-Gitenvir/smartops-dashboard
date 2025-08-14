import paramiko

# SSH login details
hostname = input("Enter Linux IP or hostname: ")
port = 22
username = input("Enter SSH username (e.g., root): ")
password = input("Enter SSH password: ")

def execute_command(command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(command)
        print("🔧 Output:\n")
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print("⚠️ Error:\n", err)

        ssh.close()
    except Exception as e:
        print("❌ Connection failed:", str(e))

def show_menu():
    while True:
        print("""
=========== Docker Command Menu ===========
1. Docker Version
2. Docker Images
3. Docker Containers (Running)
4. Docker Containers (All)
5. Pull Docker Image
6. Run Docker Container
7. Stop Docker Container
8. Remove Docker Container
9. Remove Docker Image
10. Exit
===========================================
        """)
        choice = input("Enter your choice: ")

        if choice == "1":
            execute_command("docker --version")
        elif choice == "2":
            execute_command("docker images")
        elif choice == "3":
            execute_command("docker ps")
        elif choice == "4":
            execute_command("docker ps -a")
        elif choice == "5":
            img = input("Enter image name (e.g., ubuntu:latest): ")
            execute_command(f"docker pull {img}")
        elif choice == "6":
            img = input("Image name to run: ")
            cmd = input("Command to run inside container (e.g., bash): ")
            execute_command(f"docker run -it {img} {cmd}")
        elif choice == "7":
            cid = input("Enter container ID or name to stop: ")
            execute_command(f"docker stop {cid}")
        elif choice == "8":
            cid = input("Enter container ID or name to remove: ")
            execute_command(f"docker rm {cid}")
        elif choice == "9":
            img = input("Enter image name to remove: ")
            execute_command(f"docker rmi {img}")
        elif choice == "10":
            print("✅ Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    show_menu()
