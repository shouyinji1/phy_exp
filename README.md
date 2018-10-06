# phy_exp

## Systemd

```

[Unit]
Description=QQBot Service
After=network.target
Wants=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/qqbot -u s -b /root/.qqbot-tmp/
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target

```