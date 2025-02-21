
## Nixos configuration in production environment

I use Nixos for production. Below are extracts of our configuration environment.

```nix
{ config, pkgs, lib, ... }:
let
in
{
  containers.wagtail = {
    users.users.wagtail.uid = 1003;
    users.groups.wwwrun.gid = 54;
    users.groups.wwwrun.members = ["wagtail"];
    environment.systemPackages = with pkgs; [
        ((vim_configurable.override {  }).customize{
          name = "vim";
          vimrcConfig.customRC = ''
            " your custom vimrc
            set mouse=a
            set nocompatible
            colo torte
            syntax on
            set tabstop     =2
            set softtabstop =2
            set shiftwidth  =2
            set expandtab
            set autoindent
            set smartindent
            " ...
          '';
          }
        )
        python311
        python311Packages.pillow
        python311Packages.gunicorn
        python311Packages.pip
        libjpeg
        zlib
        libtiff
        freetype
        python311Packages.venvShellHook
        curl
        wget
        lynx
        dig    
        python311Packages.pylibjpeg-libjpeg
        git
        tmux
        bat
        cowsay
        lzlib
        killall
        pwgen
        python311Packages.pypdf2
        python311Packages.python-ldap
        python311Packages.pq
        python311Packages.aiosasl
        python311Packages.psycopg2
        gettext
        sqlite
        postgresql_14
        pipx
        gnumake
        poetry
        nodejs_22
        yarn
        jq
        ];
      nix.settings.experimental-features = "nix-command flakes";
      time.timeZone = "Europe/Amsterdam";
      system.stateVersion = "24.11";
    bindMounts = { 
      "/home/wagtail/wagtail.resdigita.com/media" = { 
        hostPath = "/var/www/wagtail.resdigita.com/media";
        isReadOnly = false; 
      }; 
      "/home/wagtail/wagtail.resdigita.com/static" = { 
        hostPath = "/var/www/wagtail.resdigita.com/static";
        isReadOnly = false; 
      }; 
    };
    bindMounts = { 
      "/home/wagtail/wagtail.resdigita.com.main/media" = { 
        hostPath = "/var/www/wagtail.resdigita.com.main/media";
        isReadOnly = false; 
      }; 
      "/home/wagtail/wagtail.resdigita.com.main/static" = { 
        hostPath = "/var/www/wagtail.resdigita.com.main/static";
        isReadOnly = false; 
      }; 
    };
    systemd.services.wagtail-resdigita-com = {
      description = "wagtail.resdigita.com Website based on wagtail-news-starter";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        WorkingDirectory = "/home/wagtail/wagtail.resdigita.com/";
        ExecStart = ''/home/wagtail/wagtail.resdigita.com/venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-error.log --chdir /home/wagtail/wagtail.resdigita.com --workers 12 --bind 0.0.0.0:8902 settings.wsgi:application'';
        Restart = "always";
        RestartSec = "10s";
        EnvironmentFile = "/home/wagtail/wagtail.resdigita.com/.env";
        User = "wagtail";
        Group = "users";
      };
      unitConfig = {
        StartLimitInterval = "1min";
      };
    };
  };
    systemd.services.wagtail-resdigita-com-main = {
      description = "wagtail.resdigita.com Website from main branch based on no template";
      after = [ "network.target" ];
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
        WorkingDirectory = "/home/wagtail/wagtail.resdigita.com.main/";
        ExecStart = ''/home/wagtail/wagtail.resdigita.com.main/venv/bin/gunicorn --env WAGTAIL_ENV='production' --access-logfile /var/log/wagtail/wagtail-resdigita-com-main-access.log --error-logfile /var/log/wagtail/wagtail-resdigita-com-main-error.log --chdir /home/wagtail/wagtail.resdigita.com.main --workers 12 --bind 0.0.0.0:8903 settings.wsgi:application'';
        Restart = "always";
        RestartSec = "10s";
        EnvironmentFile = "/home/wagtail/wagtail.resdigita.com.main/.env";
        User = "wagtail";
        Group = "users";
      };
      unitConfig = {
        StartLimitInterval = "1min";
      };
    };
  };
  services.nginx.virtualHosts = {
    "wagtailnews.resdigita.com"= {
      root = "/var/www/wagtail.resdigita.com/";
      locations."/" = {
        proxyPass = "http://127.0.0.1:8902/";
        extraConfig = nginxLocationWagtailExtraConfig;
      };
      enableACME=true;
      forceSSL = true;
      locations."/favicon.ico" = { proxyPass = null; };
      locations."/static" = { proxyPass = null; };
      locations."/media" = { proxyPass = null; };
      locations."/.well-known" = { proxyPass = null; };
    };
    "wagtail.resdigita.com"= {
      root = "/var/www/wagtail.resdigita.com.main/";
      locations."/" = {
        proxyPass = "http://127.0.0.1:8903/";
        extraConfig = nginxLocationWagtailExtraConfig;
      };
      enableACME=true;
      forceSSL = true;
      locations."/favicon.ico" = { proxyPass = null; };
      locations."/static" = { proxyPass = null; };
      locations."/media" = { proxyPass = null; };
      locations."/.well-known" = { proxyPass = null; };
    };
  };
  users = {
    users = {
        wagtail = {
            isNormalUser = true;
        };
    };
    groups = {
        
    };
  };
}
```