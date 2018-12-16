.. _storage.service:

===============
storage.service
===============
-----------------------------------
/etc/systemd/system/storage.service
-----------------------------------
::

    [Unit]
    Description=storage service for Smappee
    After=network.target

    [Service]
    Environment="APP_SETTINGS=/var/www/storage/config.ini"
    ExecStart=/var/www/storage/env/bin/main --config_root Smappee start
    Restart=on-failure
    Type=simple
    User=www-storage
    Group=www-storage

    [Install]
    WantedBy=default.target

