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
ln -sfn "r-$NEW" "$WWW/current.tmp"
mv -T "$WWW/current.tmp" "$WWW/current"

# Webserver-Einstellungen übernehmen, falls geändert
if ! cmp -s server/Caddyfile /opt/ewf/Caddyfile; then
  cp server/Caddyfile /opt/ewf/Caddyfile
  docker exec ewf-caddy caddy reload --config /etc/caddy/Caddyfile >/dev/null 2>&1 || docker restart ewf-caddy >/dev/null
fi

# Nur die letzten drei Stände behalten
ls -1dt "$WWW"/r-* | tail -n +4 | xargs -r rm -rf
echo "live: $NEW"
