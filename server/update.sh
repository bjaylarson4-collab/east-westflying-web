#!/bin/sh
# Holt den neuesten Stand aus GitHub, baut die Seite und schaltet sie live.
# Läuft auf dem Server alle zwei Minuten (systemd-Timer ewf-update).
set -eu
REPO=/opt/ewf/repo
WWW=/opt/ewf/www

cd "$REPO"
git fetch -q --depth 1 origin main
NEW=$(git rev-parse FETCH_HEAD)

# Seite nur neu bauen, wenn es einen neuen Stand gibt
if ! { [ -L "$WWW/current" ] && [ "$(readlink "$WWW/current")" = "r-$NEW" ]; }; then
  git reset -q --hard "$NEW"
  python3 build.py live >/dev/null
  rm -rf "$WWW/r-$NEW"
  cp -a dist/live "$WWW/r-$NEW"
  printf "%s\n%s\n" "$NEW" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$WWW/r-$NEW/version.txt"
  # Statusdateien in den neuen Stand mitnehmen
  cp "$WWW"/current/*-check.txt "$WWW/r-$NEW/" 2>/dev/null || true
  ln -sfn "r-$NEW" "$WWW/current.tmp"
  mv -T "$WWW/current.tmp" "$WWW/current"
  # Nur die letzten drei Stände behalten
  ls -1dt "$WWW"/r-* | tail -n +4 | xargs -r rm -rf
  echo "live: $NEW"
fi

# Auslagerungsspeicher (1 GB) einmalig anlegen: Der Server hat nur 1 GB Arbeitsspeicher,
# Umami und die Datenbank brauchen zusammen mehrere hundert MB.
if [ ! -f /swapfile ]; then
  { fallocate -l 1G /swapfile && chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile \
    && echo '/swapfile none swap sw 0 0' >> /etc/fstab; } || true
fi

# Besucherstatistik (Umami) starten bzw. aktualisieren, wenn server/umami/compose.yaml geändert ist.
# Die Passwörter werden einmalig auf dem Server erzeugt und landen nie im Repository.
U=/opt/ewf/umami
if [ -f server/umami/compose.yaml ] && ! cmp -s server/umami/compose.yaml "$U/compose.yaml"; then
  mkdir -p "$U"
  if [ ! -f "$U/.env" ]; then
    ( umask 077
      printf "APP_SECRET=%s\nDB_PASSWORD=%s\n" \
        "$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')" \
        "$(head -c 24 /dev/urandom | od -An -tx1 | tr -d ' \n')" > "$U/.env" )
  fi
  if docker compose -p ewf-umami -f server/umami/compose.yaml --env-file "$U/.env" up -d >/opt/ewf/umami.log 2>&1; then
    cp server/umami/compose.yaml "$U/compose.yaml"
    echo "ok $(date -u +%FT%TZ)" > "$WWW/current/umami-check.txt"
  else
    { echo "FEHLER $(date -u +%FT%TZ) - wird beim nächsten Lauf erneut versucht"; tail -5 /opt/ewf/umami.log; } > "$WWW/current/umami-check.txt"
  fi
fi

# Webserver-Einstellungen übernehmen, falls geändert, aber nur wenn sie fehlerfrei sind
if ! cmp -s server/Caddyfile /opt/ewf/Caddyfile; then
  if docker run --rm -v "$REPO/server/Caddyfile:/etc/caddy/Caddyfile:ro" caddy:2 \
       caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/opt/ewf/caddy-check.log 2>&1; then
    cp server/Caddyfile /opt/ewf/Caddyfile
    docker restart ewf-caddy >/dev/null
    echo "ok $(date -u +%FT%TZ)" > "$WWW/current/caddy-check.txt"
  else
    { echo "FEHLER $(date -u +%FT%TZ) - bisherige Einstellungen bleiben aktiv"; tail -5 /opt/ewf/caddy-check.log; } > "$WWW/current/caddy-check.txt"
  fi
fi
