import subprocess
import sys
import os

def install():
    print("Checking system for hardware acceleration...")
    
    # Check if NVIDIA GPU exists without needing torch installed first
    try:
        gpu_check = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        has_gpu = gpu_check.returncode == 0
    except:
        has_gpu = False

    cmd = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]

    if has_gpu:
        print("🚀 NVIDIA GPU detected! Installing with CUDA support...")
    else:
        print("💻 No NVIDIA GPU found. Installing standard CPU version...")
        # Remove the extra index for non-GPU users to speed up their install
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
        with open("temp_reqs.txt", "w") as f:
            for line in lines:
                if "extra-index-url" not in line:
                    f.write(line)
        cmd = [sys.executable, "-m", "pip", "install", "-r", "temp_reqs.txt"]

    subprocess.check_call(cmd)
    
    if os.path.exists("temp_reqs.txt"):
        os.remove("temp_reqs.txt")
        
    print("\n✅ Setup complete!")

if __name__ == "__main__":
    install()