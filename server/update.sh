#!/bin/sh
# Holt den neuesten Stand aus GitHub, baut die Seite und schaltet sie live.
# Läuft auf dem Server alle zwei Minuten (systemd-Timer ewf-update).
set -eu
REPO=/opt/ewf/repo
WWW=/opt/ewf/www

cd "$REPO"
git fetch -q --depth 1 origin main
NEW=$(git rev-parse FETCH_HEAD)
[ -L "$WWW/current" ] && [ "$(readlink "$WWW/current")" = "r-$NEW" ] && exit 0

git reset -q --hard "$NEW"
python3 build.py live >/dev/null
rm -rf "$WWW/r-$NEW"
cp -a dist/live "$WWW/r-$NEW"
printf "%s\n%s\n" "$NEW" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$WWW/r-$NEW/version.txt"
ln -sfn "r-$NEW" "$WWW/current.tmp"
mv -T "$WWW/current.tmp" "$WWW/current"

# Webserver-Einstellungen übernehmen, falls geändert, aber nur wenn sie fehlerfrei sind
if ! cmp -s server/Caddyfile /opt/ewf/Caddyfile; then
  if docker run --rm -v "$REPO/server/Caddyfile:/etc/caddy/Caddyfile:ro" caddy:2 \
       caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/opt/ewf/caddy-check.log 2>&1; then
    cp server/Caddyfile /opt/ewf/Caddyfile
    docker restart ewf-caddy >/dev/null
    echo "ok $(date -u +%FT%TZ)" > "$WWW/r-$NEW/caddy-check.txt"
  else
    { echo "FEHLER $(date -u +%FT%TZ) - bisherige Einstellungen bleiben aktiv"; tail -5 /opt/ewf/caddy-check.log; } > "$WWW/r-$NEW/caddy-check.txt"
  fi
fi

# Nur die letzten drei Stände behalten
ls -1dt "$WWW"/r-* | tail -n +4 | xargs -r rm -rf
echo "live: $NEW"
