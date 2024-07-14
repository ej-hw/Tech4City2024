import subprocess

def build_and_run_docker(dockerfile_path, image_name, container_name, remove_after_run=True):
    try:
        # Step 1: Build the Docker image
        build_command = f"docker build -t {image_name} -f {dockerfile_path} ."
        print(f"Running build command: {build_command}")
        subprocess.run(build_command, check=True, shell=True)
        print(f"Successfully built Docker image '{image_name}'")

        # Step 2: Run the Docker container
        run_command = f"docker run --name {container_name} {image_name}"
        print(f"Running run command: {run_command}")
        subprocess.run(run_command, check=True, shell=True)
        print(f"Successfully started Docker container '{container_name}'")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
    finally:
        if remove_after_run:
            # Remove the container after it stops
            remove_container_command = f"docker rm {container_name}"
            print(f"Removing container: {remove_container_command}")
            subprocess.run(remove_container_command, shell=True)

            # Remove the image after container removal (optional)
            remove_image_command = f"docker rmi {image_name}"
            print(f"Removing image: {remove_image_command}")
            subprocess.run(remove_image_command, shell=True)

# Example usage
dockerfile_path = "Dockerfile"  # Path to your Dockerfile
image_name = "my_docker_image"  # Name of the Docker image
container_name = "my_docker_container"  # Name of the Docker container

build_and_run_docker(dockerfile_path, image_name, container_name)
