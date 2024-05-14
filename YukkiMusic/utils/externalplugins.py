import subprocess
import os
import shutil


def load_external_plugin(repo_url):
    destination_directory = "YukkiMusic/plugins/external"

    try:
        subprocess.run(["git", "clone", repo_url])
        repo_name = repo_url.split("/")[-1].split(".")[0]
        os.makedirs(destination_directory, exist_ok=True)
        for filename in os.listdir(repo_name):
            src = os.path.join(repo_name, filename)
            dest = os.path.join(destination_directory, filename)
            shutil.move(src, dest)
        shutil.rmtree(repo_name)
    except Exception as e:
        print("Error:", e)
