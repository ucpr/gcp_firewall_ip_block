import time
import subprocess
from subprocess import PIPE


def parse_text(filepath):
    # https://ipv4.fetus.jp/
    # ブロックしたい国のipリストをplain textでダウンロードして渡してあげる
    ip_ranges = list()

    with open(filepath, mode="r") as f:
        lines = map(lambda l: l.strip(), f.readlines()[6:])

    return lines


def create_firewall_rule(ip_ranges, rule_name, network="default", priority="100"):
    cmd = [
        "gcloud",
        "compute",
        "firewall-rules",
        "create",
        rule_name,
        "--network",
        network,
        "--action",
        "deny",
        "--direction",
        "ingress",
        "--rules",
        "tcp",
        "--source-ranges",
        ip_ranges,
        "--priority",
        priority,
    ]

    proc = subprocess.run(" ".join(cmd), shell=True, stdout=PIPE, stderr=PIPE, text=True)
    print(proc.stdout)
    print(proc.stderr)


def main():
    ip_list_filename = ""
    ip_ranges = list(parse_text(ip_list_filename))
    n = 255
    splited_ip_ranges = [",".join(ip_ranges[i: i + n]) for i in range(0, len(ip_ranges), n)]

    base_rule_name = "block"
    for idx, val in enumerate(splited_ip_ranges):
        create_firewall_rule(val, base_rule_name + str(idx))
        time.sleep(1)


if __name__ == "__main__":
    main()
