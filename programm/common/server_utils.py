import requests
import time

from common.storage import write_logs
from common.utils import unix_to_utc

def is_server_available(ip, port, timeout=20):
    try:
        response = requests.get(f"http://{ip}:{port}/ping", timeout=timeout)
        return response.status_code == 200
    except:
        return False


def send_all_files_from_folder(cd_folders: list, target_ip, target_port, mode, cd_log):
    """
    cd_folders - список путей к файлам
    mode - режим: 'pi' или 'vm'
    """
    if mode == 'pi':
        for cd_folder in cd_folders:
            if cd_folder.endswith('.wav'):
                with open(cd_folders, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"http://{target_ip}:{target_port}/receive_file", files=files)
                    write_logs(cd_log, f"Отправлен wav в {unix_to_utc(time.time())}: {cd_folder}, статус: {response.status_code}")
            elif cd_folder.endswith('.txt'):
                with open(cd_folder, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"http://{target_ip}:{target_port}/receive_file", files=files)
                    write_logs(cd_log, f"Отправлены логи PI в {unix_to_utc(time.time())}: {cd_folder}, статус: {response.status_code}")
            time.sleep(5)       


    elif mode == 'vm':
        for cd_folder in cd_folders:
            if cd_folder.endswith('.json'):
                with open(cd_folder, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"http://{target_ip}:{target_port}/receive_file", files=files)
                    write_logs(cd_log, f"\nОтправлены пролеты в {unix_to_utc(time.time())}: {cd_folder}, статус: {response.status_code}")
            elif cd_folder.endswith('.txt'):
                with open(cd_folder, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"http://{target_ip}:{target_port}/receive_file", files=files)
                    write_logs(cd_log, f"Отправлено время в {unix_to_utc(time.time())}: {cd_folder}, статус: {response.status_code}")
            time.sleep(5)
