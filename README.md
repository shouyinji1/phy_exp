# phy_exp

淮阴工学院大学物理实验课选课提醒程序


## Systemd配置
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
