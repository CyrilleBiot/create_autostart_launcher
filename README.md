# create_autostart_launcher

Juste un utilitaire pour créer un fichier de démarrage automatique d'application dans un environnement X.


## Dépendances

 python3, python3-gi, python3-pil

## Fichier crée

Le fichier sera créé dans 

```.config/autostart/```

## Contenu du paquet debian

``` tree create-autostart-launcher
create-autostart-launcher
├── debian
│   ├── changelog
│   ├── compat
│   ├── control
│   ├── copyright
│   ├── install
│   ├── postinst
│   ├── prerm
│   └── rules
└── source
    ├── apropos.png
    ├── create_autostart_launcher.6.gz
    ├── create_autostart_launcher.desktop
    └── create_autostart_launcher.py

2 directories, 12 files
```


## Screenshoots

![screenshoot](https://cbiot.fr/site/launcher_01.png)
![screenshoot](https://cbiot.fr/site/launcher_02.png)
![screenshoot](https://cbiot.fr/site/launcher_03.png)
![screenshoot](https://cbiot.fr/site/launcher_04.png)

## Changelog

create-autostart-launcher (1.2.5) unstable; urgency=medium

  * Fix bugs to the AboutDialog Box

 -- ragnarok <ragnarok@valhalla.sid-local>  Sat, 28 Nov 2020 18:10:43 +0100

create-autostart-launcher (1.2.4) unstable; urgency=medium
  * bug fix symlink postinst
  * activate and focus-out-event on the Entry Name

create-autostart-launcher (1.2.3) UNRELEASED; urgency=medium

  * buttonName add event activate. Fix bugs in Edition Mode (loop / validity filename)
 

 -- ragnarok <ragnarok@valhalla.sid-local>  Wed, 25 Nov 2020 19:00:33 +0100

create-autostart-launcher (1.1.1) unstable; urgency=medium

  * Initial release. First Package 
  * Add alert dialog boxes 

 -- ragnarok <ragnarok@valhalla.sid-local>  Mon, 23 Nov 2020 20:46:04 +0100

